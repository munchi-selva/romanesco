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
        # An example of XML (from ps_king_richard_ii.xml) and corresponding extracted sentences:
        #   <speech>
        #       <line globalnumber="588" number="306" form="verse">Then England&#8217;s ground, farewell, sweet soil, <foreign xml:lang="fr">adieu</foreign>;</line>
        #       <line globalnumber="589" number="307" form="verse">My mother, and my nurse, that bears me yet!</line>
        #       <line globalnumber="590" number="308" form="verse">Where e&#8217;er I wander, boast of this I can,</line>
        #       <line globalnumber="591" number="309" form="verse">Though banish&#8217;d, yet a true-born Englishman.</line>
        #   </speech>
        #
        #   If original linebreaks are NOT included as special tokens:
        #   Sentence 1 = Then England’s ground, farewell, sweet soil,  adieu ; My mother, and my nurse, that bears me yet!
        #   Sentence 2 = Where e’er I wander, boast of this I can, Though banish’d, yet a true-born Englishman.
        #
        #   If original linebreaks are included as special tokens:
        #   Sentence 1 = Then England’s ground, farewell, sweet soil,  adieu ; <LBR> My mother, and my nurse, that bears me yet!
        #   Sentence 2 = <LBR> Where e’er I wander, boast of this I can, <LBR> Though banish’d, yet a true-born Englishman.
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
