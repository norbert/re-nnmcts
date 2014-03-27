SHELL = /bin/sh

RESOLUTION ?= 60
DIVISOR ?= 2
BOUNDARY ?= 86400

words_files := $(foreach partition,$(PARTITIONS),$(addprefix data/words.,$(addsuffix .tsv,$(partition))))
matches_files := $(foreach klass,positive negative,$(foreach partition,$(PARTITIONS),$(addprefix data/statuses-matches.$(klass).,$(addsuffix .tsv,$(partition)))))
timestamps_files := $(foreach partition,$(PARTITIONS),$(addprefix data/statuses-timestamps.,$(addsuffix .tsv,$(partition))))
references_file := data/references.tsv
dist_files := trends-positive words-negative
dist_files := $(foreach file,$(dist_files),$(addprefix data/,$(addsuffix .dist.tsv,$(file)))) $(references_file)

all: dist
dist: $(dist_files)

data/statuses-tokens.%.tsv.bz2: data/statuses.%.json.bz2
	bzcat $< | \
		python json2tsv2.py publishedTs actor.originalId object.content object.id | \
		python tokenize-statuses.py | \
			bzip2 > $@
data/statuses-timestamps.%.tsv: | data/statuses-tokens.%.tsv.bz2
	bzcat $| | cut -f 3 | sort -n > $@

data/trends-cut.tsv: data/trends.tsv
	cat data/trends.tsv | python cut-trends.py $(MIN) $(MAX) > $@
data/trends-positive.tsv: data/trends-cut.tsv
	cat $< | python filter-trends.py -b $(BOUNDARY) $(MIN) $(MAX) | sort > $@
data/words.%.tsv: | data/statuses-tokens.%.tsv.bz2
	bzcat $| | python count-words.py > $@
data/words-negative.tsv: data/trends-cut.tsv | $(words_files)
	cat $| | python sample-tokens.py -c 500 $< | sort > $@
data/%.dist.tsv: data/%.tsv
	cut -f 1 $< | uniq > $@

data/statuses-matches.positive.%.tsv: data/trends-positive.tsv | data/statuses-tokens.%.tsv.bz2
	bzcat $| | python extract-matches.py $< > $@
data/statuses-matches.negative.%.tsv: data/words-negative.tsv | data/statuses-tokens.%.tsv.bz2
	bzcat $| | python extract-matches.py $< > $@

data/timeseries.positive.$(RESOLUTION).tsv: data/trends-positive.dist.tsv
	cat data/statuses-matches.positive.*.tsv | python extract-timeseries.py $(MIN) $(MAX) $(RESOLUTION) $< > $@
data/timeseries.negative.$(RESOLUTION).tsv: data/words-negative.dist.tsv
	cat data/statuses-matches.negative.*.tsv | python extract-timeseries.py $(MIN) $(MAX) $(RESOLUTION) $< > $@
data/timeseries.$(DIVISOR).tsv: data/timeseries.positive.$(RESOLUTION).tsv data/timeseries.negative.$(RESOLUTION).tsv
	cat $^ | python merge-timeseries.py -d $(DIVISOR) > $@

data/references.tsv: data/timeseries.$(DIVISOR).tsv data/trends-positive.tsv data/words-negative.dist.tsv
	cat $< | python write-references.py -d $(DIVISOR) $(MIN) $(MAX) $(RESOLUTION) $(wordlist 2,3,$^) > $@

clean:
	-rm -rf -- \
		data/statuses-timestamps.*.tsv \
		data/trends-cut.tsv data/trends-positive.tsv \
		data/words.*.tsv data/words-negative.tsv \
		data/timeseries.*.tsv
distclean:
	-rm -rf -- \
		$(dist_files)

.PHONY: all dist clean distclean
.DELETE_ON_ERROR:
.PRECIOUS: data/statuses-tokens.%.tsv.bz2 $(matches_files)
