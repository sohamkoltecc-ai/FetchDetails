import sys
import requests

def get_github_activity(username):
    # This URL fetches public events for any GitHub user
    url = f"https://github.com{username}/events"
    
    try:
        response = requests.get(url)
        
        # Check if user exists
        if response.status_code == 404:
            print(f"Error: User '{username}' not found.")
            return
        
        # Check for other API errors
        response.raise_for_status()
        
        events = response.json()
        if not events:
            print(f"No recent public activity found for {username}.")
            return
        
        print(f"\n🚀 Recent GitHub Activity for {username}:")
        print("-" * 40)
        
        # Pull out the 5 most recent actions
        for event in events[:5]:
            event_type = event.get('type')
            repo_name = event.get('repo', {}).get('name')
            
            # Translate cryptic API strings into clean text
            if event_type == "PushEvent":
                commits = len(event.get('payload', {}).get('commits', []))
                print(f"📝 Pushed {commits} commit(s) to {repo_name}")
            elif event_type == "IssuesEvent":
                action = event.get('payload', {}).get('action')
                print(f"⚠️ {action.capitalize()} an issue in {repo_name}")
            elif event_type == "WatchEvent":
                print(f"⭐ Starred the repository {repo_name}")
            elif event_type == "CreateEvent":
                ref_type = event.get('payload', {}).get('ref_type')
                print(f"🆕 Created a new {ref_type} in {repo_name}")
            else:
                print(f"🔔 Activity: {event_type} on {repo_name}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python github_fetcher.py <github_username>")
    else:
        get_github_activity(sys.argv[1])
