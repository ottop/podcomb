#! /bin/sh

source_dir=$(dirname "$0")

cp -r $source_dir/dist/podcomb /usr/share/podcomb
ln -s /usr/share/podcomb/podcomb /usr/bin/podcomb

cp $source_dir/eu.ottop.PodComb.desktop /usr/share/applications/eu.ottop.PodComb.desktop