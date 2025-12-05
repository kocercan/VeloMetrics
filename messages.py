# ================================================================
#  RENDER MESSAGES - ENGLISH ONLY
# ================================================================
#  All render progress messages in English for international users
# ================================================================

# ==================== RENDER PROGRESS MESSAGES ====================
MESSAGES = {
    # Startup messages
    'startup_title': "🚴 PRO VERSION v5 - MODULAR VIDEO RENDERER",
    'config_loading': "📋 Loading configuration...",
    'config_valid': "✅ Configuration is valid!",
    'config_invalid': "❌ Configuration has errors",
    'theme_loaded': "🎨 Theme loaded:",
    
    # File operations
    'file_loading': "📁 Loading files...",
    'gpx_loading': "🗺️  Loading GPX track data...",
    'gpx_loaded': "✅ GPX data loaded successfully",
    'gpx_points': "📍 Track points:",
    'video_loading': "🎬 Loading video file...",
    'video_loaded': "✅ Video loaded successfully",
    'video_info': "📺 Video info:",
    
    # Processing
    'processing_start': "🚀 Starting video processing...",
    'processing_frame': "🎬 Processing frame",
    'processing_progress': "📊 Progress:",
    'processing_complete': "✅ Processing complete!",
    'demo_mode': "🧪 Demo mode: processing first",
    'demo_seconds': "seconds only",
    
    # Data processing
    'data_interpolating': "📈 Interpolating GPS data...",
    'data_calculating': "🧮 Calculating metrics...",
    'hr_zones_calculated': "💓 Heart rate zones calculated for age",
    'power_calculating': "⚡ Calculating power data...",
    
    # Widget rendering
    'widgets_rendering': "🎨 Rendering widgets...",
    'hud_rendering': "🖥️  Rendering HUD overlay...",
    'map_rendering': "🗺️  Rendering route map...",
    'elevation_rendering': "⛰️  Rendering elevation profile...",
    'curve_applying': "🌊 Applying curve effects...",
    
    # Output
    'output_saving': "💾 Saving output video...",
    'output_saved': "✅ Output video saved:",
    'output_location': "📁 Location:",
    'output_size': "📏 File size:",
    'output_duration': "⏱️  Duration:",
    
    # Performance
    'performance_fps': "🎯 Processing speed:",
    'performance_time': "⏱️  Total time:",
    'performance_frames': "🎬 Total frames:",
    'memory_usage': "🧠 Memory usage:",
    
    # Errors and warnings
    'error_gpx_not_found': "❌ GPX file not found:",
    'error_video_not_found': "❌ Video file not found:",
    'error_processing': "❌ Error during processing:",
    'warning_config': "⚠️  Configuration warning:",
    'warning_performance': "⚠️  Performance warning:",
    
    # Cache and optimization
    'cache_loading': "🗄️  Loading cache...",
    'cache_saving': "🗄️  Saving cache...",
    'optimization_start': "⚡ Optimizing performance...",
    'vectorization_enabled': "🚀 Vectorization enabled",
    'antialiasing_enabled': "✨ Anti-aliasing enabled",
    
    # Theme and style
    'theme_applying': "🎨 Applying theme:",
    'font_loading': "🔤 Loading fonts:",
    'icons_rendering': "🎯 Rendering icons with style:",
    'curves_enabled': "🌊 Curve effects enabled",
    'curves_disabled': "📐 Flat design mode",
    
    # Completion
    'render_success': "🎉 Render completed successfully!",
    'render_failed': "💥 Render failed",
    'ready_to_play': "▶️  Ready to play:",
    'tips_title': "💡 Tips:",
    'tip_demo_mode': "• Use demo mode for quick testing",
    'tip_theme_change': "• Change themes in config.py",
    'tip_widget_disable': "• Disable unused widgets for better performance",
}

def get_message(key, *args):
    """
    Get localized message with optional formatting
    """
    message = MESSAGES.get(key, f"[Missing message: {key}]")
    if args:
        try:
            return message.format(*args)
        except:
            return f"{message} {' '.join(str(arg) for arg in args)}"
    return message

def print_message(key, *args):
    """
    Print localized message
    """
    print(get_message(key, *args))

def print_section(title_key, *args):
    """
    Print a section header with decorative lines
    """
    title = get_message(title_key, *args)
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_progress(current, total, message_key="processing_progress"):
    """
    Print progress with percentage
    """
    percentage = (current / total) * 100 if total > 0 else 0
    print(f"\r{get_message(message_key)} {current}/{total} ({percentage:.1f}%)", end="", flush=True)

def print_success(message_key, *args):
    """
    Print success message with green checkmark
    """
    print(f"✅ {get_message(message_key, *args)}")

def print_error(message_key, *args):
    """
    Print error message with red X
    """
    print(f"❌ {get_message(message_key, *args)}")

def print_warning(message_key, *args):
    """
    Print warning message with yellow warning sign
    """
    print(f"⚠️  {get_message(message_key, *args)}")

def print_info(message_key, *args):
    """
    Print info message with blue info icon
    """
    print(f"ℹ️  {get_message(message_key, *args)}")

# ==================== SPECIALIZED FORMATTERS ====================

def format_file_size(bytes_size):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def format_duration(seconds):
    """Format duration in human readable format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def format_fps(fps):
    """Format FPS with appropriate precision"""
    return f"{fps:.1f} fps"

def format_memory(bytes_mem):
    """Format memory usage"""
    return format_file_size(bytes_mem)

# ==================== RENDER STATUS REPORTER ====================

class RenderStatus:
    """
    Centralized render status reporting
    """
    def __init__(self):
        self.start_time = None
        self.current_frame = 0
        self.total_frames = 0
        
    def start_render(self, total_frames):
        """Start render timing"""
        import time
        self.start_time = time.time()
        self.total_frames = total_frames
        self.current_frame = 0
        print_section('processing_start')
        
    def update_progress(self, frame_num):
        """Update render progress"""
        self.current_frame = frame_num
        print_progress(frame_num, self.total_frames)
        
    def finish_render(self, output_path):
        """Finish render and show stats"""
        import time
        import os
        
        end_time = time.time()
        total_time = end_time - self.start_time if self.start_time else 0
        avg_fps = self.current_frame / total_time if total_time > 0 else 0
        
        print()  # New line after progress
        print_success('processing_complete')
        print_success('output_saved', output_path)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print_info('output_size', format_file_size(file_size))
            
        print_info('performance_time', format_duration(total_time))
        print_info('performance_fps', format_fps(avg_fps))
        print_info('performance_frames', self.current_frame)
        
        print_section('render_success')
        print_info('ready_to_play', output_path)

# Global render status instance
render_status = RenderStatus()