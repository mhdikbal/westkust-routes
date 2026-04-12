"""
Standalone test runner — can be executed directly with: python run_tests.py
No pytest required as fallback.
"""
import sys
import os
import traceback

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_seed_logic_tests():
    """Run all seed_data.py logic tests."""
    from seed_data import clean_name, classify_direction
    
    passed = 0
    failed = 0
    errors = []
    
    def check(test_name, actual, expected):
        nonlocal passed, failed
        if actual == expected:
            passed += 1
            print(f"  ✅ {test_name}")
        else:
            failed += 1
            msg = f"  ❌ {test_name}: expected '{expected}', got '{actual}'"
            print(msg)
            errors.append(msg)
    
    print("\n" + "="*60)
    print("TEST: clean_name()")
    print("="*60)
    
    check("simple_name", clean_name("Padang"), "Padang")
    check("comma_separated", clean_name("Batavia,Batavia"), "Batavia")
    check("comma_with_region", clean_name("Padang,Sumatra's Westkust"), "Padang")
    check("baros_to_barus", clean_name("Baros"), "Barus")
    check("airbangis", clean_name("Airbangis"), "Air Bangis")
    check("aijer_bangis", clean_name("Aijer Bangis"), "Air Bangis")
    check("djambi", clean_name("Djambi"), "Jambi")
    check("dash_prefix", clean_name("-,Bengalen"), "Bengalen")
    check("empty", clean_name(""), "")
    check("none", clean_name(None), "")
    check("palembang_comma", clean_name("Palembang,Palembang"), "Palembang")
    check("lampongs", clean_name("Lampongs"), "Lampung")
    check("unknown_passthrough", clean_name("SomeRandomPort"), "SomeRandomPort")
    
    print("\n" + "="*60)
    print("TEST: classify_direction()")
    print("="*60)
    
    check("outbound_padang_batavia", classify_direction("Padang", "Batavia"), "outbound")
    check("outbound_barus_batavia", classify_direction("Barus", "Batavia"), "outbound")
    check("outbound_air_bangis", classify_direction("Air Bangis", "Batavia"), "outbound")
    check("outbound_cingkuak", classify_direction("Pulau Cingkuak", "Batavia"), "outbound")
    check("outbound_air_haji", classify_direction("Air Haji", "Batavia"), "outbound")
    check("inbound_batavia_padang", classify_direction("Batavia", "Padang"), "inbound")
    check("inbound_jambi_padang", classify_direction("Jambi", "Padang"), "inbound")
    check("transit_palembang_batavia", classify_direction("Palembang", "Batavia"), "transit")
    check("transit_jambi_batavia", classify_direction("Jambi", "Batavia"), "transit")
    check("internal_westkust", classify_direction("Padang", "Barus"), "outbound")
    check("unknown_both", classify_direction("Bengalen", "Malabar"), "transit")
    check("outbound_to_unknown", classify_direction("Padang", "Bengalen"), "outbound")
    check("unknown_to_westkust", classify_direction("Bengalen", "Padang"), "inbound")
    
    print("\n" + "="*60)
    print("TEST: Pipeline (clean_name + classify_direction)")
    print("="*60)
    
    check("raw_padang_batavia", 
          classify_direction(clean_name("Padang"), clean_name("Batavia,Batavia")), "outbound")
    check("raw_baros_batavia", 
          classify_direction(clean_name("Baros"), clean_name("Batavia,Batavia")), "outbound")
    check("raw_palembang_batavia", 
          classify_direction(clean_name("Palembang,Palembang"), clean_name("Batavia,Batavia")), "transit")
    check("raw_padang_bengalen", 
          classify_direction(clean_name("Padang"), clean_name("-,Bengalen")), "outbound")
    check("raw_djambi_batavia", 
          classify_direction(clean_name("Djambi"), clean_name("Batavia,Batavia")), "transit")
    
    print("\n" + "="*60)
    total = passed + failed
    if failed == 0:
        print(f"🎉 ALL {total} TESTS PASSED!")
    else:
        print(f"⚠️  {passed}/{total} passed, {failed} FAILED")
        for e in errors:
            print(e)
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    try:
        success = run_seed_logic_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
