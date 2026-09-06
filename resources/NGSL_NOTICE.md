# NGSL 1.2 attribution and modification notice

`ngsl_1_2_ascii_forms.json` is derived from the New General Service List 1.2
statistics and research-lemmatized files by Charles Browne, Brent Culligan, and
Joseph Phillips, downloaded from the [official NGSL Project
site](https://www.newgeneralservicelist.com/new-general-service-list).

The source list is licensed under [Creative Commons Attribution-ShareAlike 4.0
International](https://creativecommons.org/licenses/by-sa/4.0/). This modified
projection retains each source-supplied ASCII alphabetic form, all of its NGSL
head-lemma mappings, and the head lemmas' source SFI ranks. Thus `found`,
`left`, `mine`, `rose`, and `wound` retain two possible heads instead of being
silently collapsed. The projection lowercases forms and excludes seven
hyphenated variants because this profile's declared tokenizer treats hyphens as
boundaries and the source also supplies their unhyphenated forms.

NGSL research forms deliberately disregard meaning sense and identify
homographs that require researcher adjustment. Membership or rank therefore
does not establish contextual meaning, learner knowledge, CEFR level, or a
Nation BNC/COCA word-family level. See `RIGHTS.md` and the embedded profile
manifest for hashes, exact processing, limitations, and removal instructions.
