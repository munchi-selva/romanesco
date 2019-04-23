#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# Extracts text from XML-formatted Shakespeare plays for LM training.
#
# Author: Margaret Chi
###############################################################################


################################################################################
# Imports
################################################################################
import argparse
import glob
import io
import lxml.etree as ET
import nltk
import os
import re


################################################################################
# Module-wide constants
################################################################################
#
# XML tags from the PlayShakespeare schema
#
PS_TAG_TITLE   = "title"
PS_TAG_SPEECH  = "speech"
PS_TAG_LINE    = "line"

#
# Directory and file handling
#
SCRIPT_DIR      = os.path.dirname(os.path.realpath(__file__))
XML_CONTENT_DIR = SCRIPT_DIR + "/../extracted_data/xml_content/"
XML_CONTENT_EXT  = ".xml.content"
SENT_OUTPUT_DIR = SCRIPT_DIR + "/../extracted_data/play_sents/"
SENT_OUTPUT_EXT = ".sents"

#
# Output formatting
#
LINE_BREAK = "<LBR>"


###############################################################################
def getPlaySents(playFilename: str, sentFilename: str,
                 appendToFile: bool = False, includeLineBreaks: bool = False):
    """
    Extracts sentences for LM training from an XML-formatted Shakespeare play.

    :param playFilename: Name of the XML file
    :param sentFilename: Name of an output file for the sentences
    :param appendToFile: Whether to append to or overwrite an existing copy of
                         the output file
    :param includeLineBreaks: Whether to use a special token to mark the
                              original linebreaks
    :returns: The sentences
    """
    outputFilemode = "a" if appendToFile else "w"
    lineJoinSeq = (" " + LINE_BREAK  + " ") if includeLineBreaks else " "

    sents = []

    with open(playFilename, "r") as playXMLFile:
        playTree = ET.parse(playXMLFile).getroot()
        #
        # Include the play's title as the first sentence
        #
        sents.append(playTree.findall(PS_TAG_TITLE)[0].text)

        #
        # Locate each speech in the play.
        # Combine the lines from the speech into a single block of text.
        # Split the block into individual sentences, using NLTK's sentence
        # tokenizer. This works relatively well for Shakespearean text.
        #
        for speech in playTree.findall(PS_TAG_SPEECH):
            #
            # itertext() includes the textual content of children of the line element
            #
            speechContent = lineJoinSeq.join([" ".join(line.itertext()) for line in speech.findall(PS_TAG_LINE)])
            speechSents   = nltk.sent_tokenize(speechContent)
            sents += speechSents

    with io.open(sentFilename, mode = outputFilemode, buffering = -1, encoding = "utf-8") as playSentFile:
        for sent in sents:
            playSentFile.write(u"{}\n".format(sent))

    return sents
###############################################################################


###############################################################################
def main():
    """
    Extracts sentences for LM training from XML-formatted Shakespeare plays.

    :returns: None
    """
    #
    # Command-line argument processing, temporarily disabled because
    # argparse store_false isn't setting the linebreaks option to false
    #
    argParser = argparse.ArgumentParser(description = "Shakespearean sentence extractor")
    argParser.add_argument("-l", "--linebreaks",
                           help = "include original linebreaks in extracted sentences",
                           action = "store_true", default = "false")
    args = argParser.parse_args()
    includeLineBreaks = args.linebreaks

    outputFileExtension = SENT_OUTPUT_EXT
    if includeLineBreaks:
        outputFileExtension = outputFileExtension + ".lb"

    #
    # Ensure the output directory exists
    #
    if not os.path.exists(SENT_OUTPUT_DIR):
        os.makedirs(SENT_OUTPUT_DIR)

    #
    # Extract sentences for all xml content files
    #
    playFilenames = sorted(glob.glob("{}*{}".format(XML_CONTENT_DIR, XML_CONTENT_EXT)))
    for playFilename in playFilenames:
        playShortFilename = os.path.basename(playFilename)
        playName = playShortFilename.replace(XML_CONTENT_EXT, '')
        sentFilename = "{}{}{}".format(SENT_OUTPUT_DIR, playName, outputFileExtension)
        sents = getPlaySents(playFilename, sentFilename,
                             includeLineBreaks = includeLineBreaks)
###############################################################################
 

if __name__ == "__main__":
    main()
