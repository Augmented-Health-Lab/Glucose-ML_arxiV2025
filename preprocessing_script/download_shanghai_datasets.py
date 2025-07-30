import requests
import os

def download_figshare_collection(collection_url):
    """
    Downloads all files from a Figshare collection.

    Args:
        collection_url (str): The URL of the Figshare collection.
    """
    try:
        collection_id = collection_url.strip().split('/')[-1]
        if not collection_id.isdigit():
            print("Error: Unable to extract valid collection ID from URL.")
            return

        api_base_url = "https://api.figshare.com/v2"
        collection_api_url = f"{api_base_url}/collections/{collection_id}/articles"

        print(f"Getting file list from collection ID: {collection_id}...")

        # Get all articles in the collection
        response = requests.get(collection_api_url)
        response.raise_for_status()  # Raise exception if request fails
        articles = response.json()

        if not articles:
            print("No articles found in this collection.")
            return

        total_files = 0
        # Iterate through each article to download its files
        for article in articles:
            article_id = article['id']
            article_api_url = f"{api_base_url}/articles/{article_id}/files"
            
            files_response = requests.get(article_api_url)
            files_response.raise_for_status()
            files = files_response.json()

            for file_info in files:
                total_files += 1
                file_url = file_info['download_url']
                file_name = file_info['name']
                file_path = os.path.join("../Original datasets", file_name)

                print(f"\nDownloading file: {file_name}...")

                # Use stream=True to handle large files
                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                        
        if total_files == 0:
             print("No downloadable files found in the collection's articles.")

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
    except KeyError as e:
        print(f"Error parsing API response: missing key {e}")
    except Exception as e:
        print(f"Unknown error occurred: {e}")

if __name__ == "__main__":
    target_collection_url = "https://figshare.com/collections/Diabetes_Datasets_ShanghaiT1DM_and_ShanghaiT2DM/6310860"
    
    download_figshare_collection(target_collection_url)