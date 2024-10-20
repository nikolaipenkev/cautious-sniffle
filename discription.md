Script Explanation

Reading the File: The script opens and reads the rt-feed-record file line by line, parsing each line as JSON.

Counting Distinct Stories: It maintains a set of unique RP_DOCUMENT_ID values to count the total number of distinct stories.

Tracking Analytics: For each story, it tracks the expected number of analytics (DOCUMENT_RECORD_COUNT) and the indices of received analytics (DOCUMENT_RECORD_INDEX). This information is stored in a dictionary for later analysis.

Detecting Missing Analytics: After processing all lines, the script checks for any missing indices by comparing the expected indices (from 1 to DOCUMENT_RECORD_COUNT) with the indices that were received. It generates a report of any missing analytics.

Validating RP_ENTITY_ID: The script also validates the format of the RP_ENTITY_ID field using a regular expression. It prints a message for any invalid entries.

Outputting Results: Finally, the script prints the total number of distinct stories and a report detailing any missing analytics for each story.