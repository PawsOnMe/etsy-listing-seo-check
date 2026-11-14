# etsy-listing-seo-check

A free checker for Etsy listing titles and tags.

It catches what Etsy won't accept: a title over 140 characters, more than 13 tags, a tag over 20 characters, or a tag with characters Etsy doesn't allow. It also flags a few common weak spots: empty tag slots, one-word tags, duplicate tags, a word used three times in the title, and a main keyword sitting at the end of the title.

It's one Python file. No install, no API key, and nothing leaves your computer.

Made by **PawsOnMePet**, a small Etsy shop of ceramic slow feeder bowls for cats and dogs: https://www.etsy.com/shop/PawsOnMePet. These are the same rules we follow for our own listings.

## Try it

```
python3 scripts/etsy_seo_check.py --file examples/slow-feeder-bowl.json
```

```
Title: 125/140 characters | Tags: 12/13
  x [tag-too-long] "ceramic slow feeder dish" is 24 characters. Etsy allows 20 per tag.
  ! [unused-tag-slots] 1 tag slot(s) left empty. Each tag is one more phrase a buyer can find you with.
  ! [duplicate-tag] "cat bowl" is used 2 times.
  ! [single-word-tag] "bowl" is one word. A short phrase like "slow feeder bowl" is closer to what buyers type.
  ! [title-repeats] Used 3+ times in the title: cat. Swap a repeat for a new phrase.
1 error(s), 4 warning(s)
```

Check your own listing:

```
python3 scripts/etsy_seo_check.py \
  --title "Your listing title" \
  --tags "tag one, tag two, tag three" \
  --keyword "the phrase buyers search"
```

Add `--json` for machine-readable output. The exit code is 1 when Etsy would reject something.

## Use it with an AI agent

The folder is a ready-made agent skill (`SKILL.md`). In Claude Code, copy the folder into `~/.claude/skills/` and ask "check my Etsy title and tags". Other agents can be pointed at `SKILL.md`.

## What it checks

| Check | Level | Where the rule comes from |
|---|---|---|
| Title is 140 characters or less | error | [Etsy Help: How to Create a Listing](https://help.etsy.com/hc/en-us/articles/115015628707-How-to-Create-a-Listing) |
| 13 tags or fewer | error | [Etsy Help: How to Use Tags](https://help.etsy.com/hc/en-us/articles/360000336307-How-to-Use-Tags-to-Get-Found-in-Search) |
| Each tag is 20 characters or less | error | same page |
| Tags use letters, numbers and spaces; ' and - only inside a word | error | same page |
| Empty tag slots | warning | our rule of thumb |
| Duplicate tags | warning | our rule of thumb |
| One-word tags | warning | our rule of thumb |
| A word used 3+ times in the title | warning | our rule of thumb |
| Main keyword missing from the title | warning | our rule of thumb |
| Main keyword starts after character 40 | info | our rule of thumb |
| All-caps words of 4+ letters | info | our rule of thumb |

The rules of thumb are ours, not Etsy policy. The checker doesn't estimate search volume or ranking. For that, use Etsy's search bar suggestions or a keyword tool.

## License

MIT
