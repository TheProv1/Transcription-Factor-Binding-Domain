# Transcription-Factor-Binding-Domain

## Project Overview

This project is a collection of Python scripts designed to perform a multi-stage analysis on a hierarchically organized dataset of transcription factor protein sequences. The pipeline automates the process of parsing raw data, extracting functionally relevant protein domains, analyzing their biophysical properties, and visualizing their sequence composition.

## Dataset Description/Information

This dataset is hierarchically organised as superclass-class-family-subfamily

for example, the file *1.1.1.1.txt* will be refered to as belonging to superclass 1, class 1, family 1, sub-family 1

Each subfamily contains one or more *.txt* files, and within each *.txt* file there exists 2 or more transcription factors, each transcription factor is a long chain of amino acids which has only one DBD region

**DBD Region** - Refers to the region where the protien binds to the DNA which in turn activates/enables gene expression
**Non-DBD Region** - Region where the protien does not bind to DNA

It is hyposized that the DBD region is ordered, while the Non-DBD region is unordered

In order, to separate the transcription factors from each other from a *.txt* file, we keep checking the **POS** Header in the file, when the previous value is less than the current value, we stop and consider it as a transciption factor. This process continues till the end of the file

## Script Description

##### Complete Window Script

This script iterates from window sizes 3-11, and uses a sliding window approach to count the number of occurences of an amino acid chain along each indivitual transcription factor. The output is stored a directory called *output/* with directories within it labelled with the window count

##### DBD Disorder Script



##### DBD Splitting Script



##### Amino Acid Distribution Script


