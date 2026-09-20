import Foundation
import ScreenCaptureKit
@main struct Main {
 static func main() async throws {
  let content = try await SCShareableContent.excludingDesktopWindows(true, onScreenWindowsOnly: false)
  for window in content.windows where window.owningApplication?.bundleIdentifier == "com.google.Chrome" && (window.title ?? "").contains("FlowPy") {
   print("WINDOW \(window.windowID) \(window.frame.width)x\(window.frame.height) \(window.title ?? "")")
  }
 }
}
