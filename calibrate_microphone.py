#!/usr/bin/env python3
"""
JARVIS Microphone Calibration Tool
Run this script to optimize your microphone settings for better voice recognition
"""

from modules.mic_calibration import MicrophoneCalibrator

def main():
    """Main calibration function"""
    print("🎤 JARVIS Microphone Calibration Tool")
    print("="*50)
    print("This tool will help you optimize your microphone settings")
    print("for better voice recognition with JARVIS.\n")
    
    print("Before starting:")
    print("• Make sure your microphone is connected")
    print("• Close other applications that might use the microphone")
    print("• Find a reasonably quiet environment")
    print("• Have your microphone at normal speaking distance\n")
    
    input("Press Enter when ready to start calibration...")
    
    calibrator = MicrophoneCalibrator()
    results = calibrator.full_calibration()
    
    if results:
        print(f"\n🎯 QUICK SETUP GUIDE:")
        print(f"Your optimal energy threshold is: {results['optimal_threshold']:.0f}")
        print(f"Environment noise level: {results['noise_level']}")
        print(f"Voice recognition rate: {results['success_rate']:.1f}%")
        
        if results['success_rate'] >= 80:
            print("\n✅ Excellent! Your microphone is well calibrated for JARVIS.")
        elif results['success_rate'] >= 60:
            print("\n⚠️  Good setup, but there's room for improvement.")
        else:
            print("\n❌ Your setup needs attention for optimal JARVIS performance.")
        
        print(f"\nThe continuous listener will automatically use these optimized settings.")
    else:
        print("\n❌ Calibration incomplete. Please check your microphone setup and try again.")
    
    print(f"\nTo run JARVIS with optimized settings:")
    print(f"python jarvis.py")

if __name__ == "__main__":
    main()