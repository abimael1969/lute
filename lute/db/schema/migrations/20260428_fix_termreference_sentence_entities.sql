-- Clean up term reference sentences that were double-escaped before display.

UPDATE termreferences
SET TrSentenceHTML = replace(
  replace(
    replace(
      replace(
        replace(TrSentenceHTML, '&amp;#39;', '&#39;'),
        '&amp;quot;', '&quot;'
      ),
      '&amp;amp;', '&amp;'
    ),
    '&amp;lt;', '&lt;'
  ),
  '&amp;gt;', '&gt;'
)
WHERE TrSentenceHTML LIKE '%&amp;#39;%'
   OR TrSentenceHTML LIKE '%&amp;quot;%'
   OR TrSentenceHTML LIKE '%&amp;amp;%'
   OR TrSentenceHTML LIKE '%&amp;lt;%'
   OR TrSentenceHTML LIKE '%&amp;gt;%';
