import Foundation
import AppKit
import ScreenCaptureKit
import AVFoundation

final class Recorder: NSObject, SCStreamOutput, SCStreamDelegate, @unchecked Sendable {
    let writer: AVAssetWriter
    let input: AVAssetWriterInput
    let metadata: URL
    var firstPTS: CMTime?
    var firstEpoch: Double = 0
    var frames = 0
    init(path: String, metadata: String, width: Int, height: Int) throws {
        self.metadata = URL(fileURLWithPath: metadata)
        writer = try AVAssetWriter(outputURL: URL(fileURLWithPath: path), fileType: .mp4)
        input = AVAssetWriterInput(mediaType: .video, outputSettings: [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: width, AVVideoHeightKey: height, AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 5000000, AVVideoExpectedSourceFrameRateKey: 15, AVVideoMaxKeyFrameIntervalKey: 30]])
        input.expectsMediaDataInRealTime = true
        writer.add(input)
        super.init()
    }
    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .screen, sampleBuffer.isValid else { return }
        guard let attachments = CMSampleBufferGetSampleAttachmentsArray(sampleBuffer, createIfNecessary: false) as? [[SCStreamFrameInfo: Any]], let raw = attachments.first?[.status] as? Int, SCFrameStatus(rawValue: raw) == .complete else { return }
        if firstPTS == nil {
            firstPTS = sampleBuffer.presentationTimeStamp
            firstEpoch = Date().timeIntervalSince1970
            writer.startWriting()
            writer.startSession(atSourceTime: firstPTS!)
            let data = try! JSONSerialization.data(withJSONObject: ["first_frame_epoch":firstEpoch,"width":1920,"height":914], options:.prettyPrinted)
            try! data.write(to:metadata)
            print("RECORDING_READY \(firstEpoch)"); fflush(stdout)
        }
        if input.isReadyForMoreMediaData { input.append(sampleBuffer); frames += 1 }
    }
    func stream(_ stream: SCStream, didStopWithError error: Error) { print("CAPTURE_ERROR \(error)"); fflush(stdout) }
    func finish() async {
        input.markAsFinished()
        await writer.finishWriting()
        print("RECORDING_DONE frames=\(frames) status=\(writer.status.rawValue)")
    }
}

@main struct Main {
    static func main() async throws {
        _ = NSApplication.shared
        let args=CommandLine.arguments
        guard args.count >= 6 else { print("record_window WINDOW_ID OUTPUT META STOPFILE PAGE_HEIGHT"); return }
        let windowID=UInt32(args[1])!
        let content=try await SCShareableContent.excludingDesktopWindows(true,onScreenWindowsOnly:false)
        guard let window=content.windows.first(where:{$0.windowID==windowID && $0.owningApplication?.bundleIdentifier=="com.google.Chrome" && ($0.title ?? "").contains("FlowPy")}) else { throw NSError(domain:"FlowPy",code:1,userInfo:[NSLocalizedDescriptionKey:"Dedicated FlowPy Chrome window not found"])}
        let pageHeight=Double(args[5])!
        let width=1920, height=Int((pageHeight/window.frame.width*1920)/2)*2
        let recorder=try Recorder(path:args[2],metadata:args[3],width:width,height:height)
        let config=SCStreamConfiguration()
        config.width=width;config.height=height
        config.minimumFrameInterval=CMTime(value:1,timescale:15)
        config.queueDepth=5;config.showsCursor=true;config.capturesAudio=false
        config.ignoreShadowsSingleWindow=true
        config.sourceRect=CGRect(x:0,y:window.frame.height-pageHeight,width:window.frame.width,height:pageHeight)
        let filter=SCContentFilter(desktopIndependentWindow:window)
        let stream=SCStream(filter:filter,configuration:config,delegate:recorder)
        try stream.addStreamOutput(recorder,type:.screen,sampleHandlerQueue:DispatchQueue(label:"flowpy.capture"))
        try await stream.startCapture()
        while !FileManager.default.fileExists(atPath:args[4]) { try await Task.sleep(nanoseconds:200_000_000) }
        try await stream.stopCapture()
        await recorder.finish()
    }
}
