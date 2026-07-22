import AppKit

private let frameCount = 6
private let petSize = CGFloat(210)
private let attackReach = CGFloat(88)
private let catchDistance = CGFloat(125)
private let escapeDistance = CGFloat(165)
private let maximumSpeed = CGFloat(11)

final class PetController: NSObject, NSApplicationDelegate {
    private var window: NSWindow!
    private var imageView: NSImageView!
    private var statusItem: NSStatusItem!
    private var timer: Timer?
    private var walkFrames: [NSImage] = []
    private var fightFrames: [NSImage] = []
    private var petPosition = NSPoint.zero
    private var frameIndex = 0
    private var tickCount = 0
    private var facingRight = true
    private var fighting = false

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)

        walkFrames = loadFrames(named: "leo-walk-v2")
        fightFrames = loadFrames(named: "leo-fight")

        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: petSize, height: petSize),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = false
        window.level = .floating
        window.ignoresMouseEvents = true
        window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .stationary]

        imageView = NSImageView(frame: window.contentView!.bounds)
        imageView.autoresizingMask = [.width, .height]
        imageView.imageScaling = .scaleProportionallyUpOrDown
        imageView.wantsLayer = true
        window.contentView?.addSubview(imageView)

        let mouse = NSEvent.mouseLocation
        petPosition = NSPoint(x: mouse.x - petSize / 2, y: mouse.y - petSize - 25)
        window.setFrameOrigin(petPosition)
        window.orderFrontRegardless()

        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "figure.walk", accessibilityDescription: "Leo")
            button.toolTip = "Leo's Desktop Buddy"
        }
        let menu = NSMenu()
        let info = NSMenuItem(title: "Leo is following your mouse", action: nil, keyEquivalent: "")
        info.isEnabled = false
        menu.addItem(info)
        menu.addItem(.separator())
        menu.addItem(NSMenuItem(title: "Exit", action: #selector(quit), keyEquivalent: "q"))
        statusItem.menu = menu

        timer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { [weak self] _ in
            self?.tick()
        }
    }

    @objc private func quit() {
        NSApp.terminate(nil)
    }

    private func tick() {
        let mouse = NSEvent.mouseLocation
        let center = NSPoint(x: petPosition.x + petSize / 2, y: petPosition.y + petSize / 2)
        let cursorDX = mouse.x - center.x
        let cursorDY = mouse.y - center.y
        let cursorDistance = hypot(cursorDX, cursorDY)

        fighting = fighting ? cursorDistance < escapeDistance : cursorDistance < catchDistance
        if !fighting && abs(cursorDX) > 3 { facingRight = cursorDX > 0 }

        let targetX = mouse.x + (facingRight ? -attackReach : attackReach)
        let targetY = mouse.y - 28
        let dx = targetX - center.x
        let dy = targetY - center.y
        let distance = hypot(dx, dy)

        if !fighting && distance > 7 {
            let speed = min(maximumSpeed, max(2.2, distance * 0.055))
            petPosition.x += dx / distance * speed
            petPosition.y += dy / distance * speed
            if tickCount % 5 == 0 { frameIndex = (frameIndex + 1) % frameCount }
        } else if fighting {
            if tickCount % 7 == 0 { frameIndex = (frameIndex + 1) % frameCount }
        } else {
            frameIndex = 1
        }

        let bob = !fighting && distance <= 7 ? CGFloat(sin(Double(tickCount) / 9.0) * 2) : 0
        window.setFrameOrigin(NSPoint(x: petPosition.x, y: petPosition.y + bob))

        let frames = fighting ? fightFrames : walkFrames
        imageView.image = frames[frameIndex]
        imageView.layer?.setAffineTransform(
            facingRight ? .identity : CGAffineTransform(scaleX: -1, y: 1)
        )
        window.orderFrontRegardless()
        tickCount += 1
    }

    private func loadFrames(named name: String) -> [NSImage] {
        guard let url = Bundle.main.url(forResource: name, withExtension: "png"),
              let sheet = NSImage(contentsOf: url),
              let representation = sheet.representations.first else {
            fatalError("Missing animation resource: \(name).png")
        }

        let pixelWidth = representation.pixelsWide
        let pixelHeight = representation.pixelsHigh
        let cellWidth = pixelWidth / frameCount

        return (0..<frameCount).map { index in
            let source = NSRect(
                x: CGFloat(index * cellWidth),
                y: 0,
                width: CGFloat(cellWidth),
                height: CGFloat(pixelHeight)
            )
            let frame = NSImage(size: source.size)
            frame.lockFocus()
            NSGraphicsContext.current?.imageInterpolation = .high
            sheet.draw(
                in: NSRect(origin: .zero, size: source.size),
                from: source,
                operation: .copy,
                fraction: 1
            )
            frame.unlockFocus()
            return frame
        }
    }

    func applicationWillTerminate(_ notification: Notification) {
        timer?.invalidate()
    }
}

let app = NSApplication.shared
let controller = PetController()
app.delegate = controller
app.run()
