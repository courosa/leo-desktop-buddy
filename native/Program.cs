using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

namespace LeoDesktopBuddy
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            bool created;
            using (var mutex = new Mutex(true, @"Local\LeoDesktopBuddy_SingleInstance", out created))
            {
                if (!created) return;
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                Application.Run(new LeoPetForm());
            }
        }
    }

    internal sealed class LeoPetForm : Form
    {
        private const int FrameCount = 6;
        private const int PetSize = 180;
        private const double AttackReach = 78;
        private const double CatchDistance = 112;
        private const double EscapeDistance = 150;
        private const double MaxSpeed = 10.5;

        private readonly Bitmap[] walkRight;
        private readonly Bitmap[] walkLeft;
        private readonly Bitmap[] fightRight;
        private readonly Bitmap[] fightLeft;
        private readonly System.Windows.Forms.Timer timer;
        private readonly NotifyIcon trayIcon;

        private double petX;
        private double petY;
        private int frameIndex;
        private int tickCount;
        private bool facingRight = true;
        private bool fighting;

        [StructLayout(LayoutKind.Sequential)]
        private struct NativePoint { public int X; public int Y; }

        [DllImport("user32.dll")]
        private static extern bool GetCursorPos(out NativePoint point);

        protected override CreateParams CreateParams
        {
            get
            {
                const int WS_EX_TOOLWINDOW = 0x00000080;
                const int WS_EX_TRANSPARENT = 0x00000020;
                const int WS_EX_NOACTIVATE = 0x08000000;
                var cp = base.CreateParams;
                cp.ExStyle |= WS_EX_TOOLWINDOW | WS_EX_TRANSPARENT | WS_EX_NOACTIVATE;
                return cp;
            }
        }

        public LeoPetForm()
        {
            Text = "Leo's Desktop Buddy";
            ClientSize = new Size(PetSize, PetSize);
            FormBorderStyle = FormBorderStyle.None;
            StartPosition = FormStartPosition.Manual;
            ShowInTaskbar = false;
            TopMost = true;
            BackColor = Color.Lime;
            TransparencyKey = Color.Lime;
            DoubleBuffered = true;

            walkRight = LoadFrames("LeoDesktopBuddy.assets.sprites.leo-walk-v2.png");
            walkLeft = MirrorFrames(walkRight);
            fightRight = LoadFrames("LeoDesktopBuddy.assets.sprites.leo-fight.png");
            fightLeft = MirrorFrames(fightRight);

            NativePoint cursor;
            GetCursorPos(out cursor);
            petX = cursor.X - PetSize / 2.0;
            petY = cursor.Y + 30;
            Location = new Point((int)petX, (int)petY);

            var menu = new ContextMenuStrip();
            menu.Items.Add("Leo is following your mouse").Enabled = false;
            menu.Items.Add(new ToolStripSeparator());
            menu.Items.Add("Exit", null, delegate { Close(); });

            trayIcon = new NotifyIcon
            {
                Text = "Leo's Desktop Buddy",
                Icon = CreateTrayIcon(),
                ContextMenuStrip = menu,
                Visible = true
            };

            timer = new System.Windows.Forms.Timer { Interval = 16 };
            timer.Tick += OnTick;
            timer.Start();
        }

        protected override bool ShowWithoutActivation { get { return true; } }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Bitmap[] frames = fighting
                ? (facingRight ? fightRight : fightLeft)
                : (facingRight ? walkRight : walkLeft);
            e.Graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
            e.Graphics.DrawImageUnscaled(frames[frameIndex], 0, 0);
        }

        private void OnTick(object sender, EventArgs e)
        {
            NativePoint cursor;
            if (!GetCursorPos(out cursor)) return;

            double centerX = petX + PetSize / 2.0;
            double centerY = petY + PetSize / 2.0;
            double cursorDx = cursor.X - centerX;
            double cursorDy = cursor.Y - centerY;
            double cursorDistance = Math.Sqrt(cursorDx * cursorDx + cursorDy * cursorDy);

            fighting = fighting ? cursorDistance < EscapeDistance : cursorDistance < CatchDistance;
            if (!fighting && Math.Abs(cursorDx) > 3) facingRight = cursorDx > 0;

            double targetX = cursor.X + (facingRight ? -AttackReach : AttackReach);
            double targetY = cursor.Y + 28;
            double dx = targetX - centerX;
            double dy = targetY - centerY;
            double distance = Math.Sqrt(dx * dx + dy * dy);

            if (!fighting && distance > 7)
            {
                double speed = Math.Min(MaxSpeed, Math.Max(2.2, distance * 0.055));
                petX += dx / distance * speed;
                petY += dy / distance * speed;
                if (tickCount % 5 == 0) frameIndex = (frameIndex + 1) % FrameCount;
            }
            else if (fighting)
            {
                if (tickCount % 7 == 0) frameIndex = (frameIndex + 1) % FrameCount;
            }
            else
            {
                frameIndex = 1;
            }

            int bob = !fighting && distance <= 7 ? (int)(Math.Sin(tickCount / 9.0) * 2) : 0;
            Location = new Point((int)Math.Round(petX), (int)Math.Round(petY + bob));
            Invalidate();
            tickCount++;
        }

        private static Bitmap[] LoadFrames(string resourceName)
        {
            Assembly assembly = Assembly.GetExecutingAssembly();
            using (Stream stream = assembly.GetManifestResourceStream(resourceName))
            {
                if (stream == null) throw new InvalidOperationException("Missing animation: " + resourceName);
                using (var sheet = new Bitmap(stream))
                {
                    int cellWidth = sheet.Width / FrameCount;
                    var frames = new Bitmap[FrameCount];
                    for (int i = 0; i < FrameCount; i++)
                    {
                        var cell = new Rectangle(i * cellWidth, 0, cellWidth, sheet.Height);
                        Rectangle bounds = FindAlphaBounds(sheet, cell);
                        var frame = new Bitmap(PetSize, PetSize);
                        using (Graphics graphics = Graphics.FromImage(frame))
                        {
                            graphics.Clear(Color.Transparent);
                            graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                            double scale = Math.Min((PetSize - 8.0) / bounds.Width, (PetSize - 8.0) / bounds.Height);
                            int width = Math.Max(1, (int)Math.Round(bounds.Width * scale));
                            int height = Math.Max(1, (int)Math.Round(bounds.Height * scale));
                            int x = (PetSize - width) / 2;
                            int y = PetSize - height - 2;
                            graphics.DrawImage(sheet, new Rectangle(x, y, width, height), bounds, GraphicsUnit.Pixel);
                        }
                        frames[i] = frame;
                    }
                    return frames;
                }
            }
        }

        private static Rectangle FindAlphaBounds(Bitmap bitmap, Rectangle area)
        {
            int left = area.Right, top = area.Bottom, right = area.Left, bottom = area.Top;
            for (int y = area.Top; y < area.Bottom; y += 2)
            {
                for (int x = area.Left; x < area.Right; x += 2)
                {
                    if (bitmap.GetPixel(x, y).A < 8) continue;
                    left = Math.Min(left, x); top = Math.Min(top, y);
                    right = Math.Max(right, x); bottom = Math.Max(bottom, y);
                }
            }
            return right >= left ? Rectangle.FromLTRB(left, top, right + 1, bottom + 1) : area;
        }

        private static Bitmap[] MirrorFrames(Bitmap[] originals)
        {
            var mirrored = new Bitmap[originals.Length];
            for (int i = 0; i < originals.Length; i++)
            {
                mirrored[i] = (Bitmap)originals[i].Clone();
                mirrored[i].RotateFlip(RotateFlipType.RotateNoneFlipX);
            }
            return mirrored;
        }

        private static Icon CreateTrayIcon()
        {
            var bitmap = new Bitmap(32, 32);
            using (Graphics g = Graphics.FromImage(bitmap))
            using (var blue = new SolidBrush(Color.FromArgb(38, 125, 245)))
            using (var white = new Pen(Color.White, 2))
            {
                g.SmoothingMode = SmoothingMode.AntiAlias;
                g.FillEllipse(blue, 1, 1, 30, 30);
                g.FillEllipse(Brushes.White, 9, 10, 4, 4);
                g.FillEllipse(Brushes.White, 19, 10, 4, 4);
                g.DrawArc(white, 9, 12, 14, 10, 15, 150);
            }
            return Icon.FromHandle(bitmap.GetHicon());
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                timer?.Dispose();
                if (trayIcon != null) { trayIcon.Visible = false; trayIcon.Dispose(); }
                DisposeFrames(walkRight); DisposeFrames(walkLeft);
                DisposeFrames(fightRight); DisposeFrames(fightLeft);
            }
            base.Dispose(disposing);
        }

        private static void DisposeFrames(Bitmap[] frames)
        {
            if (frames == null) return;
            foreach (Bitmap frame in frames) frame.Dispose();
        }
    }
}
