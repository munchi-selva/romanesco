#!/bin/bash

#
# Retrieves XML-formatted Shakespeare plays, then extracts their spoken
# content (actual dialogue), plus a minimal number of elements required to
# produce well-formed XML output.
#

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source_rep_dir=${script_dir}/../source_xml
source_xml_dir=${source_rep_dir}/playshakespeare_editions
output_xml_dir=${script_dir}/../extracted_data/xml_content

#
# Clone PlayShakespeare XML repository, if required
#
if [ ! -d $source_rep_dir ]
then
    git clone https://github.com/severdia/PlayShakespeare.com-XML $source_rep_dir
fi

#
# Create directory to house XML play content files
#
if [ ! -d $output_xml_dir ]
then
    mkdir -p $output_xml_dir
fi


for source_xml in   ps_alls_well_that_ends_well.xml \
                    ps_antony_cleopatra.xml \
                    ps_as_you_like_it.xml \
                    ps_comedy_of_errors.xml \
                    ps_coriolanus.xml \
                    ps_cymbeline.xml \
                    ps_hamlet.xml \
                    ps_henry_iv_pt1.xml \
                    ps_henry_iv_pt2.xml \
                    ps_henry_v.xml \
                    ps_henry_vi_pt1.xml \
                    ps_henry_vi_pt2.xml \
                    ps_henry_vi_pt3.xml \
                    ps_henry_viii.xml \
                    ps_julius_caesar.xml \
                    ps_king_john.xml \
                    ps_king_lear.xml \
                    ps_king_richard_ii.xml \
                    ps_loves_labours_lost.xml \
                    ps_macbeth.xml \
                    ps_measure_for_measure.xml \
                    ps_merchant_of_venice.xml \
                    ps_merry_wives_of_windsor.xml \
                    ps_midsummer_nights_dream.xml \
                    ps_much_ado_about_nothing.xml \
                    ps_othello.xml \
                    ps_pericles.xml \
                    ps_richard_iii.xml \
                    ps_romeo_and_juliet.xml \
                    ps_taming_of_the_shrew.xml \
                    ps_tempest.xml \
                    ps_timon_of_athens.xml \
                    ps_titus_andronicus.xml \
                    ps_troilus_and_cressida.xml \
                    ps_twelfth_night.xml \
                    ps_two_gentlemen_of_verona.xml \
                    ps_winters_tale.xml
do
    source_xml_fullname=${source_xml_dir}/$source_xml
    output_xml=${output_xml_dir}/${source_xml}.content
    grep -P "(<?xml)|(<\/?(play\b|title|speech|line))" $source_xml_fullname > $output_xml
done
