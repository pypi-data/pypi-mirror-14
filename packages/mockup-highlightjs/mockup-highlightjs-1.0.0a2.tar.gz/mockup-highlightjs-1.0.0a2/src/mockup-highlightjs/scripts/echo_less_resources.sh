#!/bin/bash
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create less files
. ${CWD}/make_less.sh 1>/dev/null

cd ${CWD}/../js/less
for i in *.less; do
    style="${i%.*}"
    echo "  <records prefix=\"plone.resources/mockup-styles-highlightjs-${style}\"
            interface='Products.CMFPlone.interfaces.IResourceRegistry'>
    <value key=\"css\">
        <element>++plone++highlightjs/less/${style}.less</element>
    </value>
  </records>"
done