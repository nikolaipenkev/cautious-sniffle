import json
import re
from collections import defaultdict

# Function to process the JSON lines and analyze the data
def process_rt_feed(file_path):
    # Set to track distinct stories
    distinct_stories = set()

    # Dictionary to track story analytics
    story_analytics = defaultdict(lambda: {'expected_count': 0, 'received_indices': set()})

    # Regex pattern to validate the RP_ENTITY_ID
    rp_entity_id_pattern = re.compile(r'^[A-Za-z0-9]{10,20}$')  # Example regex pattern

    with open(file_path, 'r') as f:
        for line in f:
            try:
                # Parse each line as JSON
                analytic = json.loads(line.strip())

                # Extract required fields
                rp_document_id = analytic.get('RP_DOCUMENT_ID')
                record_index = analytic.get('DOCUMENT_RECORD_INDEX')
                record_count = analytic.get('DOCUMENT_RECORD_COUNT')
                rp_entity_id = analytic.get('RP_ENTITY_ID')

                # Add story ID to the set of distinct stories
                distinct_stories.add(rp_document_id)

                # Update expected count and received indices for each story
                story_analytics[rp_document_id]['expected_count'] = max(
                    story_analytics[rp_document_id]['expected_count'], record_count
                )
                story_analytics[rp_document_id]['received_indices'].add(record_index)

                # Validate RP_ENTITY_ID format
                if not rp_entity_id_pattern.match(rp_entity_id):
                    print(f"Invalid RP_ENTITY_ID format: {rp_entity_id}")

            except json.JSONDecodeError:
                print(f"Error parsing line: {line}")
            except KeyError as e:
                print(f"Missing expected field: {e}")

    # Check for missing analytics
    missing_analytics_report = []

    for story_id, analytics in story_analytics.items():
        expected_count = analytics['expected_count']
        received_indices = analytics['received_indices']

        # Determine missing indices by comparing expected and received ones
        missing_indices = set(range(1, expected_count + 1)) - received_indices

        if missing_indices:
            missing_analytics_report.append({
                'RP_DOCUMENT_ID': story_id,
                'missing_indices': sorted(missing_indices)
            })

    # Return distinct stories count and missing analytics report
    return {
        'total_distinct_stories': len(distinct_stories),
        'missing_analytics': missing_analytics_report
    }

# Main function to run the analysis
def main():
    file_path = './rt-feed-record'  # Path to the rt-feed-record file in the project folder

    # Process the rt-feed-record file
    result = process_rt_feed(file_path)

    # Output the results
    print(f"Total distinct stories: {result['total_distinct_stories']}")
    print("Missing analytics report:")
    for report in result['missing_analytics']:
        print(f"RP_DOCUMENT_ID: {report['RP_DOCUMENT_ID']}, Missing Indices: {report['missing_indices']}")

if __name__ == '__main__':
    main()
