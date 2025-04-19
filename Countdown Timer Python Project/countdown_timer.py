import time
import sys
import select
from typing import Optional
import os

class CountdownTimer:
    """A feature-rich countdown timer with multiple display modes and controls."""
    
    def __init__(self, theme="default"):
        """Initialize timer with default settings."""
        self.remaining = 0
        self.paused = False
        self.running = False
        self.start_time = 0
        self.end_time = 0
        self.theme = theme
        self.presets = self._load_presets()
        
    def _load_presets(self):
        """Load saved timer presets."""
        presets = {"Quick Break": 300, "Pomodoro": 1500, "Meeting": 1800}
        if os.path.exists("timer_presets.txt"):
            try:
                with open("timer_presets.txt", "r") as f:
                    for line in f:
                        if ":" in line:
                            name, seconds = line.strip().split(":", 1)
                            presets[name] = int(seconds)
            except Exception:
                pass
        return presets
        
    def save_preset(self, name, seconds):
        """Save a new timer preset."""
        self.presets[name] = seconds
        try:
            with open("timer_presets.txt", "a") as f:
                f.write(f"{name}:{seconds}\n")
            return True
        except Exception:
            return False

    def _clear_line(self):
        """Clear the current line in terminal."""
        sys.stdout.write("\033[K")  # ANSI escape code to clear line

    def _display_time(self, seconds: int) -> str:
        """Format time for display with different units based on duration."""
        if seconds >= 3600:  # 1 hour or more
            hours, remainder = divmod(seconds, 3600)
            mins, secs = divmod(remainder, 60)
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        else:
            mins, secs = divmod(seconds, 60)
            return f"{mins:02d}:{secs:02d}"

    def _get_user_input(self) -> Optional[int]:
        """Get and validate user input for timer duration."""
        # Show available presets
        if self.presets:
            print("\nAvailable presets:")
            for name, seconds in self.presets.items():
                print(f"  • {name}: {self._display_time(seconds)}")
                
        while True:
            try:
                user_input = input("\nEnter countdown time (seconds), preset name, or 'q' to quit: ").strip()
                
                if user_input.lower() in ('q', 'quit'):
                    return None
                    
                # Check if input is a preset name
                if user_input in self.presets:
                    return self.presets[user_input]
                
                # Check if it's a new preset to save
                if ":" in user_input:
                    preset_name, preset_value = user_input.split(":", 1)
                    try:
                        seconds = int(preset_value)
                        if seconds <= 0:
                            print("❌ Please enter a positive number for the preset!")
                            continue
                        self.save_preset(preset_name.strip(), seconds)
                        print(f"✅ Saved preset '{preset_name.strip()}'")
                        return seconds
                    except ValueError:
                        print("❌ Invalid preset format! Use 'name:seconds'")
                        continue
                
                # Try parsing as direct seconds input
                seconds = int(user_input)
                if seconds <= 0:
                    print("❌ Please enter a positive number!")
                    continue
                    
                return seconds
            except ValueError:
                print("❌ Invalid input! Please enter a number, preset name, or 'q' to quit.")

    def _show_progress_bar(self, elapsed: int, total: int):
        """Display a visual progress bar."""
        progress = min(1.0, elapsed / total)
        bar_length = 40
        
        # Theme-based bar style
        if self.theme == "colorful":
            chars = ['🟩', '🟨', '⬜']
            filled = int(round(bar_length * progress))
            remaining = bar_length - filled
            bar = chars[0] * filled + chars[2] * remaining
        elif self.theme == "minimal":
            bar = '▓' * int(round(bar_length * progress)) + '░' * (bar_length - int(round(bar_length * progress)))
        else:  # default
            bar = '█' * int(round(bar_length * progress)) + '-' * (bar_length - int(round(bar_length * progress)))
            
        percent = round(100 * progress)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()

    def _show_controls(self):
        """Display available controls during countdown."""
        print("\n⌨️  Controls: [P]ause | [R]esume | [S]top | [Q]uit | [+]Add 1min | [-]Remove 1min")

    def _handle_user_control(self):
        """Check for and process user control inputs."""
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            cmd = sys.stdin.readline().strip().lower()
            
            if cmd == 'p' and not self.paused:
                self.paused = True
                print("\n⏸  Timer paused")
            elif cmd == 'r' and self.paused:
                self.paused = False
                # Adjust remaining time based on pause duration
                self.end_time = time.time() + self.remaining
                print("\n▶️  Timer resumed")
            elif cmd == '+':
                # Add one minute
                self.end_time += 60
                self.remaining += 60
                print("\n⏱  Added 1 minute")
            elif cmd == '-':
                # Remove one minute (but don't go below zero)
                if self.remaining > 60:
                    self.end_time -= 60
                    self.remaining -= 60
                    print("\n⏱  Removed 1 minute")
                else:
                    print("\n⚠️  Can't reduce timer below 0")
            elif cmd in ('s', 'q'):
                self.running = False
                return cmd
        return None

    def _play_notification(self):
        """Play sound notification when timer ends."""
        try:
            # ASCII bell character (may work on some terminals)
            print('\a')
            
            # Try to use system commands as fallback
            if sys.platform.startswith('linux'):
                os.system('spd-say "Time is up"')
            elif sys.platform == 'darwin':  # macOS
                os.system('say "Time is up"')
            elif sys.platform == 'win32':  # Windows
                os.system('powershell -c (New-Object Media.SoundPlayer).PlaySync()')
        except:
            # Silently fail if sound doesn't work
            pass

    def run(self):
        """Main timer execution loop."""
        print("\n" + "=" * 50)
        print(" 🕒 COUNTDOWN TIMER 🕒 ".center(50, "="))
        print("=" * 50)
        
        # Theme selection
        print("\nTheme options: default, colorful, minimal")
        theme_choice = input("Select theme (or press Enter for default): ").strip().lower()
        if theme_choice in ["colorful", "minimal"]:
            self.theme = theme_choice
        
        while True:
            duration = self._get_user_input()
            if duration is None:
                break
                
            self.remaining = duration
            self.start_time = time.time()
            self.end_time = self.start_time + duration
            self.running = True
            self.paused = False
            
            print(f"\n▶️ Starting {self._display_time(duration)} countdown...")
            self._show_controls()
            
            try:
                while self.running and self.remaining > 0:
                    if not self.paused:
                        current_time = time.time()
                        self.remaining = max(0, self.end_time - current_time)
                        
                        # Display both digital and progress bar
                        self._clear_line()
                        print(f"⏱ Time remaining: {self._display_time(int(self.remaining))}", end=" ")
                        self._show_progress_bar(duration - int(self.remaining), duration)
                        
                        control_result = self._handle_user_control()
                        if control_result == 'q':
                            print("\n🛑 Timer cancelled by user")
                            return
                        elif control_result == 's':
                            print("\n🛑 Timer stopped")
                            break
                    
                    time.sleep(0.1)  # More responsive to controls
                
                if not self.paused and self.remaining <= 0:
                    self._clear_line()
                    print("\n⏰ Time's up! 🎉")
                    self._play_notification()
                    
                    # Flash the display
                    for _ in range(3):
                        print("\r⏰ TIME'S UP! " + "🔔" * 3, end="")
                        time.sleep(0.5)
                        print("\r" + " " * 20, end="")
                        time.sleep(0.5)
                    print("\r")
                
                print("\n✅ Countdown complete!")
            except KeyboardInterrupt:
                print("\n\n🛑 Timer interrupted")
            
            restart = input("🔄 Start another timer? (y/n): ").lower()
            if restart not in ('y', 'yes'):
                break

if __name__ == "__main__":
    try:
        timer = CountdownTimer()
        timer.run()
        print("\n👋 Thanks for using the timer! Goodbye")
    except KeyboardInterrupt:
        print("\n\n🛑 Timer stopped by user")
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("⚠️ This timer requires Unix-like system for best experience")