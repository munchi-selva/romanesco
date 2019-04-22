#!/bin/bash

#
# Collates sentences from Shakespeare's plays according to genre,
# i.e. comedy, history, tragedy, and combinations thereof.
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source_sent_dir=${script_dir}/../extracted_data/play_sents
output_sent_dir=${script_dir}/../extracted_data/play_sents_by_genre


#
# Ensure output directory exists
#
if [ ! -d $output_sent_dir ]
then
    mkdir -p $output_sent_dir
fi

#
# Genres: two sentence files should be generated for each (one copy will
# encode the linebreaks from the original play text)
#
genres="comedies \
        histories \
        tragedies \
        comhist \
        comtrag \
        histtrag \
        all"

#
# Remove previous versions of output files
#
for genre in $genres
do
    for file_ext in sents sents.lb
    do
        output_file=${output_sent_dir}/${genre}.${file_ext}
        if [ -e $output_file ]
        then
            rm $output_file
        fi
    done
done


#
# Variables name after the genres allow the plays included by each genere to
# looked up with ! syntax, e.g. ${!comedies} gives the list of comedy plays
#
comedies="ps_alls_well_that_ends_well \
          ps_as_you_like_it \
          ps_comedy_of_errors \
          ps_loves_labours_lost \
          ps_measure_for_measure \
          ps_merchant_of_venice \
          ps_merry_wives_of_windsor \
          ps_midsummer_nights_dream \
          ps_much_ado_about_nothing \
          ps_taming_of_the_shrew \
          ps_tempest \
          ps_twelfth_night \
          ps_two_gentlemen_of_verona \
          ps_winters_tale"

histories="ps_henry_iv_pt1 \
           ps_henry_iv_pt2 \
           ps_henry_v \
           ps_henry_vi_pt1 \
           ps_henry_vi_pt2 \
           ps_henry_vi_pt3 \
           ps_henry_viii \
           ps_king_john \
           ps_king_richard_ii \
           ps_pericles \
           ps_richard_iii"

tragedies="ps_antony_cleopatra \
           ps_coriolanus \
           ps_cymbeline \
           ps_hamlet \
           ps_julius_caesar \
           ps_king_lear \
           ps_macbeth \
           ps_othello \
           ps_romeo_and_juliet \
           ps_timon_of_athens \
           ps_titus_andronicus \
           ps_troilus_and_cressida"

comhist="$comedies \
         $histories"

comtrag="$comedies \
         $tragedies"

histtrag="$histories \
          $tragedies"

all="$comedies \
     $histories \
     $tragedies"

#
# For each genre, concatenate the sentences from all its plays
#
for genre in $genres
do
    for file_ext in sents sents.lb
    do
        output_file=${output_sent_dir}/${genre}.${file_ext}
        for play in ${!genre}
        do
            source_sent_file=${source_sent_dir}/${play}.${file_ext}
            if [ -e $source_sent_file ]
            then
                cat $source_sent_file >> ${output_file}
            fi
        done
    done
done
