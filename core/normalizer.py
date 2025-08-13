from typing import List, Optional, Set
from models.schemas import GENDER, ACTIVITY, WORKOUT_TYPES

def normalize_token(token: str) -> str:
    """Normalize a string token by lowercasing and replacing spaces with underscores"""
    return token.lower().strip().replace(" ", "_")

def norm_gender(x: Optional[str]) -> Optional[str]:
    """Normalize gender string to male/female/other/prefer_not_to_say"""
    if not x:
        return None
        
    x = normalize_token(x)
    
    # Map common variations
    gender_map = {
        "m": "male",
        "f": "female",
        "male": "male",
        "female": "female",
        "man": "male",
        "woman": "female",
        "masculine": "male",
        "feminine": "female"
    }
    
    return gender_map.get(x, "other" if x not in ["prefer_not_to_say", "other"] else x)

def one_of(x: Optional[str], allowed: List[str]) -> Optional[str]:
    """Match a normalized token to one value in an allowlist"""
    if not x:
        return None
        
    # Create normalized lookup
    allowed_map = {normalize_token(val): val for val in allowed}
    
    # Try to match normalized input
    normalized = normalize_token(x)
    return allowed_map.get(normalized)

def many_of(xs: List[str], allowed: List[str]) -> List[str]:
    """Deduplicate and filter multiple values against an allowlist"""
    if not xs:
        return []
        
    # Create normalized lookup
    allowed_map = {normalize_token(val): val for val in allowed}
    
    # Use set for deduplication while maintaining order of first appearance
    seen: Set[str] = set()
    result: List[str] = []
    
    for x in xs:
        normalized = normalize_token(x)
        if normalized in allowed_map and normalized not in seen:
            seen.add(normalized)
            result.append(allowed_map[normalized])
            
    return result

# Test assertions
if __name__ == "__main__":
    assert norm_gender("M") == "male", "Failed to normalize 'M' to 'male'"
    assert one_of("Very Active", ACTIVITY) == "very_active", "Failed to normalize 'Very Active' to 'very_active'"
    assert many_of(["HIIT", "yoga", "spinning"], WORKOUT_TYPES) == ["HIIT", "yoga"], \
        "Failed to correctly filter and dedupe workout types"
    print("All tests passed!")
