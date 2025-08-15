#!/usr/bin/env python3
"""
Microphone Calibration Utility
Helps users calibrate their microphone sensitivity for optimal JARVIS performance
"""

import speech_recognition as sr
import time
import statistics

class MicrophoneCalibrator:
    def __init__(self):
        """Initialize microphone calibrator"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def test_ambient_noise(self, duration=5):
        """
        Test ambient noise levels
        
        Args:
            duration: How long to sample ambient noise
        """
        print(f"Testing ambient noise for {duration} seconds...")
        print("Please remain quiet during this test.")
        
        noise_levels = []
        
        try:
            with self.microphone as source:
                for i in range(duration):
                    print(f"Sampling... {i+1}/{duration}")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                    noise_levels.append(self.recognizer.energy_threshold)
                    time.sleep(0.1)
            
            avg_noise = statistics.mean(noise_levels)
            max_noise = max(noise_levels)
            min_noise = min(noise_levels)
            
            print(f"\nAmbient Noise Analysis:")
            print(f"Average noise level: {avg_noise:.1f}")
            print(f"Maximum noise level: {max_noise:.1f}")
            print(f"Minimum noise level: {min_noise:.1f}")
            
            # Recommend threshold
            recommended_threshold = max(avg_noise * 1.5, 400)
            print(f"Recommended energy threshold: {recommended_threshold:.1f}")
            
            return {
                'average': avg_noise,
                'maximum': max_noise,
                'minimum': min_noise,
                'recommended_threshold': recommended_threshold
            }
            
        except Exception as e:
            print(f"Error during noise testing: {e}")
            return None
    
    def test_voice_levels(self, num_tests=3):
        """
        Test voice levels by having user speak
        
        Args:
            num_tests: Number of voice tests to perform
        """
        print(f"\nTesting voice levels ({num_tests} tests)...")
        print("When prompted, say 'Jarvis what time is it' clearly.")
        
        voice_levels = []
        successful_recognitions = []
        
        for i in range(num_tests):
            try:
                print(f"\nTest {i+1}/{num_tests}: Say 'Jarvis what time is it' now...")
                
                with self.microphone as source:
                    # Brief ambient adjustment
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    initial_threshold = self.recognizer.energy_threshold
                    
                    # Listen for speech
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    
                    # Record the energy level during speech
                    voice_levels.append(initial_threshold)
                
                # Try to recognize what was said
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized: '{text}'")
                    successful_recognitions.append(text.lower())
                except sr.UnknownValueError:
                    print("Could not understand speech")
                except sr.RequestError as e:
                    print(f"Recognition error: {e}")
                
            except sr.WaitTimeoutError:
                print("No speech detected - try speaking louder or closer to microphone")
            except Exception as e:
                print(f"Error during voice test {i+1}: {e}")
        
        if voice_levels:
            avg_voice = statistics.mean(voice_levels)
            max_voice = max(voice_levels)
            min_voice = min(voice_levels)
            
            print(f"\nVoice Level Analysis:")
            print(f"Average voice level: {avg_voice:.1f}")
            print(f"Maximum voice level: {max_voice:.1f}")
            print(f"Minimum voice level: {min_voice:.1f}")
            
            # Check recognition success rate
            jarvis_detected = sum(1 for text in successful_recognitions if 'jarvis' in text)
            success_rate = (jarvis_detected / len(successful_recognitions)) * 100 if successful_recognitions else 0
            
            print(f"Wake word detection rate: {jarvis_detected}/{len(successful_recognitions)} ({success_rate:.1f}%)")
            
            return {
                'average': avg_voice,
                'maximum': max_voice,
                'minimum': min_voice,
                'success_rate': success_rate,
                'recognitions': successful_recognitions
            }
        
        return None
    
    def recommend_settings(self, noise_data, voice_data):
        """
        Recommend optimal microphone settings
        
        Args:
            noise_data: Results from ambient noise test
            voice_data: Results from voice level test
        """
        print(f"\n{'='*50}")
        print("MICROPHONE CALIBRATION RECOMMENDATIONS")
        print(f"{'='*50}")
        
        if not noise_data or not voice_data:
            print("❌ Insufficient data for recommendations")
            return
        
        # Calculate optimal threshold
        noise_avg = noise_data['average']
        voice_avg = voice_data['average']
        
        # Threshold should be above noise but below voice
        if voice_avg > noise_avg:
            optimal_threshold = noise_avg + (voice_avg - noise_avg) * 0.3
        else:
            optimal_threshold = max(noise_avg * 1.5, 400)
        
        print(f"🎤 RECOMMENDED SETTINGS:")
        print(f"   Energy Threshold: {optimal_threshold:.0f}")
        print(f"   Dynamic Adjustment: Enabled")
        print(f"   Damping Factor: 0.15")
        
        # Environment assessment
        noise_level = "HIGH" if noise_avg > 800 else "MEDIUM" if noise_avg > 400 else "LOW"
        print(f"\n🌍 ENVIRONMENT ASSESSMENT:")
        print(f"   Noise Level: {noise_level}")
        print(f"   Voice Recognition: {voice_data['success_rate']:.1f}%")
        
        # Recommendations based on results
        print(f"\n💡 RECOMMENDATIONS:")
        
        if noise_avg > 800:
            print("   • High ambient noise detected")
            print("   • Consider using JARVIS in a quieter environment")
            print("   • Move closer to microphone when speaking")
            print("   • Check for fans, AC, or other noise sources")
        
        if voice_data['success_rate'] < 70:
            print("   • Low wake word detection rate")
            print("   • Speak more clearly and distinctly")
            print("   • Ensure microphone is not muted or blocked")
            print("   • Check microphone permissions in Windows")
        
        if voice_avg < noise_avg * 2:
            print("   • Voice level too close to noise level")
            print("   • Speak louder or move closer to microphone")
            print("   • Reduce background noise if possible")
        
        print(f"\n✅ Calibration complete!")
        return {
            'optimal_threshold': optimal_threshold,
            'noise_level': noise_level,
            'success_rate': voice_data['success_rate']
        }
    
    def full_calibration(self):
        """Run complete microphone calibration"""
        print("JARVIS Microphone Calibration Tool")
        print("="*40)
        print("This tool will help optimize your microphone settings for JARVIS.")
        print("Please ensure your microphone is connected and working.\n")
        
        # Test ambient noise
        noise_data = self.test_ambient_noise(duration=3)
        
        if noise_data:
            # Test voice levels
            voice_data = self.test_voice_levels(num_tests=3)
            
            if voice_data:
                # Provide recommendations
                recommendations = self.recommend_settings(noise_data, voice_data)
                return recommendations
        
        print("❌ Calibration failed. Please check your microphone setup.")
        return None

def main():
    """Run microphone calibration"""
    calibrator = MicrophoneCalibrator()
    calibrator.full_calibration()

if __name__ == "__main__":
    main()