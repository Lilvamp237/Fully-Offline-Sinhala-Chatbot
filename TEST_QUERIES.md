# Test Queries for Improved Sri Lankan Fact Bot

## Test Categories

### 1. Sri Lankan Domain-Specific Queries
These should retrieve facts from facts.json and respond with "ශ්‍රී ලංකා ගැනේ සරල දැනුම අනුව..."

- "ශ්‍රී ලංකාවේ අගනුවර කුමක්ද?"
- "ශ්‍රී ලංකාවේ උසම කන්ද?"
- "ශ්‍රී ලංකාවට නිදහස ලැබුණේ කවදාද?"
- "ශ්‍රී ලංකාවේ ජාතික ක්‍රීඩාව කුමක්ද?"
- "කොලඹ ශ්‍රී ලංකාවේ කුමන නගරයි?"

### 2. General Knowledge / Math Queries
These should use general knowledge and respond with "ගිණුම් ගැනේ දැනුම අනුව..."

- "2 + 2 එකින්න?"
- "ලොවේ මහා පනත්?"
- "Einstein කවුද?"
- "ජල මාර්ගයේ දිනුම?"
- "4 x 5 එකින්න?"

### 3. Out-of-Domain Queries
Bot should respond with "මට එම ගැන දැනීමක් නැත" or use general knowledge

- "හිජ්ර ගිණුම්?"
- "ඔබේ හිතුම?"
- "Unicode එකින්ම?"

## Expected Behavior

✅ **Accuracy improved** - Facts from database are retrieved correctly
✅ **Dual-mode support** - Both Sri Lankan facts AND general knowledge work
✅ **Confidence indicators** - Responses clearly show source (facts vs general knowledge)
✅ **Better retrieval** - k=5 with relevance filtering prevents low-quality matches
✅ **Language quality** - Responses in professional Sinhala with proper terminology

## How to Test

1. Run the bot: `streamlit run talk_talk_sinhala_bot.py`
2. Ask queries from each category
3. Verify:
   - Sri Lankan queries are accurate
   - Math/general knowledge queries work
   - Confidence indicators are shown
   - Responses are in Sinhala
   - No hallucinations or made-up facts
