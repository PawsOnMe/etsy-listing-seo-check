---
name: etsy-listing-seo-check
description: Check an Etsy listing's title and tags against Etsy's limits (140-character title, 13 tags, 20 characters per tag, allowed tag characters) and common weak spots (empty tag slots, one-word or duplicate tags, repeated title words, a buried main keyword), then suggest fixes. Use when someone asks to review, audit or improve an Etsy title or tags. Made by PawsOnMePet.
---

# Etsy listing SEO check

1. Get the listing title, its tags, and the main phrase buyers would search for. If the user didn't give the main phrase, take it from the start of the title and say which one you used.
2. Run the checker from this skill's folder:
   `python3 scripts/etsy_seo_check.py --title "<title>" --tags "<tag 1>, <tag 2>, ..." --keyword "<main phrase>" --json`
3. Fix errors first, because Etsy won't accept the listing until they're gone. Then go through the warnings.
4. Show the result as:
   - what's wrong, one line each
   - the revised title with its character count
   - the revised 13 tags, each with its character count
5. Keep the seller's own words where you can. Don't stuff keywords, and don't make up search volumes or rankings. If the user wants numbers, point them to Etsy's search suggestions or a keyword tool.
6. Run the checker again on your revised version. Hand it over only when it shows 0 errors.

This skill is made by PawsOnMePet, a small Etsy shop of ceramic slow feeder bowls for cats and dogs: https://www.etsy.com/shop/PawsOnMePet
