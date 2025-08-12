#!/usr/bin/env python3
"""
Test all TTS engines to find the best one for your system
"""

def test_windows_sapi():
    """Test Windows SAPI TTS"""
    print("Testing Windows SAPI TTS...")
    try:
        from modules.windows_tts import WindowsTTS
        
        tts = WindowsTTS()
        if not tts.initialize():
            return False
        
        success = tts.speak("Testing Windows SAPI text to speech")
        tts.cleanup()
        return success
        
    except Exception as e:
        print(f"Windows SAPI error: {e}")
        return False

def test_edge_tts():
    """Test Edge TTS"""
    print("Testing Edge TTS...")
    try:
        from modules.edge_tts import EdgeTTS
        
        tts = EdgeTTS()
        if not tts.initialize():
            return False
        
        success = tts.speak("Testing Edge neural text to speech")
        tts.cleanup()
        return success
        
    except Exception as e:
        print(f"Edge TTS error: {e}")
        return False

def test_simple_tts():
    """Test Simple TTS (pyttsx3)"""
    print("Testing Simple TTS...")
    try:
        from modules.simple_tts import SimpleTTS
        
        tts = SimpleTTS()
        if not tts.initialize():
            return False
        
        success = tts.speak("Testing simple pyttsx3 text to speech")
        tts.cleanup()
        return success
        
    except Exception as e:
        print(f"Simple TTS error: {e}")
        return False

def test_smart_tts():
    """Test Smart TTS (all engines)"""
    print("Testing Smart TTS Manager...")
    try:
        from modules.smart_tts import SmartTTS
        
        tts = SmartTTS()
        if not tts.initialize():
            return False
        
        print(f"Available engines: {tts.get_engine_info()}")
        
        # Test the smart TTS
        success = tts.speak("Testing smart TTS with automatic fallback")
        
        # Test all engines
        all_success = tts.test_all_engines()
        
        tts.cleanup()
        return success and all_success
        
    except Exception as e:
        print(f"Smart TTS error: {e}")
        return False

def main():
    """Test all TTS engines"""
    print("TTS Engine Comparison Test")
    print("=" * 40)
    
    tests = [
        ("Windows SAPI TTS", test_windows_sapi),
        ("Edge TTS (Neural)", test_edge_tts),
        ("Simple TTS (pyttsx3)", test_simple_tts),
        ("Smart TTS Manager", test_smart_tts)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 40)
    print("TTS ENGINE TEST RESULTS")
    print("=" * 40)
    
    working_engines = []
    for test_name, result in results.items():
        status = "✓ WORKING" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            working_engines.append(test_name)
    
    print(f"\nWorking engines: {len(working_engines)}")
    
    if working_engines:
        print("\n🎉 Recommended TTS engines (in order):")
        recommendations = [
            "Windows SAPI TTS",      # Most reliable
            "Smart TTS Manager",     # Best overall
            "Edge TTS (Neural)",     # Best quality
            "Simple TTS (pyttsx3)"   # Fallback
        ]
        
        for rec in recommendations:
            if rec in working_engines:
                print(f"  1. {rec}")
                break
        
        print("\n✅ Jarvis should work with TTS!")
        print("Run: python jarvis.py")
        
    else:
        print("\n❌ No TTS engines working. Possible solutions:")
        print("1. Install Edge TTS: pip install edge-tts")
        print("2. Check Windows audio settings")
        print("3. Restart Windows audio service")
        print("4. Update audio drivers")

if __name__ == "__main__":
    main()