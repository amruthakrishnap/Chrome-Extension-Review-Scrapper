from playwright.sync_api import sync_playwright
from supabase import create_client, Client
from bs4 import BeautifulSoup
import re

# Supabase configuration
url = 'Replace Your Supabase URL HERE'
key = 'Replace Your Supabase Anon (Key) Here'
supabase: Client = create_client(url, key)
# link = 'https://chromewebstore.google.com/detail/chatgpt-organize-with-fol/jijhgfapogfphcccjlpoiphpjgedblpo/reviews'
link=input("Enter Chrome Extention Review Link : ")
def main():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the page
        page.goto(link)

        # Click "Load more" button and wait for content to load
        while True:
            try:
                # Click the "Load more" button
                load_more_button = page.query_selector('button:has-text("Load more")')
                if load_more_button:
                    load_more_button.click()
                    page.wait_for_timeout(2000)  # Wait for 2 seconds to load more content
                else:
                    break
            except Exception as e:
                print("No more 'Load more' button found or an error occurred:", e)
                break

        # Get the updated page content
        html = page.content()

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract data using BeautifulSoup
        names = [item.get_text(strip=True) for item in soup.find_all(class_='LfYwpe')]
        dates = [item.get_text(strip=True) for item in soup.find_all(class_='ydlbEf')]
        ratings = [item.get('aria-label', '').strip() for item in soup.find_all(class_='B1UG8d')]
        reviews = [item.get_text(strip=True) for item in soup.find_all(class_='fzDEpf')]
        helpfuls = [item.get_text(strip=True) for item in soup.find_all(class_='ZRk0Tb')]

        # Extract additional data
        extension_name_elements = soup.find_all(class_='Pa2dE')
        extension_url_elements = soup.find_all('a', class_='KgGEHd')  # Updated to match 'a' tags with class 'KgGEHd'
        developer_elements = soup.find_all(class_='cJI8ee')
        overall_rating_elements = soup.find_all(class_=['GlMWqe', 'SxpA2e'])
        total_rating_elements = soup.find_all(class_='PloaX')
        extension_type_elements = soup.find_all(class_=['gqpEIe', 'bgp7Ye'])
        developer_details_elements = soup.find_all('a', class_='cJI8ee')
        total_users_elements = soup.find_all(class_='F9iKBc')

        # Debugging: Print out found elements
        # print(f"Found extension name elements: {len(extension_name_elements)}")
        # print(f"Found extension URL elements: {len(extension_url_elements)}")
        # print(f"Found developer elements: {len(developer_elements)}")
        # print(f"Found overall rating elements: {len(overall_rating_elements)}")
        # print(f"Found total rating elements: {len(total_rating_elements)}")
        # print(f"Found extension type elements: {len(extension_type_elements)}")
        # print(f"Found developer details elements: {len(developer_details_elements)}")
        # print(f"Found total users elements: {len(total_users_elements)}")

        extension_name = extension_name_elements[0].get_text(strip=True) if extension_name_elements else 'No name found'
        if extension_url_elements:
            href = extension_url_elements[0].get('href', '').strip()
            extension_url = 'https://chromewebstore.google.com' + href.lstrip('.') if href else 'No URL found'
        else:
            extension_url = 'No URL found'

        developer = developer_elements[0].get_text(strip=True) if developer_elements else 'No developer found'
        overall_rating = overall_rating_elements[0].get_text(strip=True) if overall_rating_elements else 'No rating found'
        total_rating = total_rating_elements[0].get_text(strip=True) if total_rating_elements else 'No total rating found'

        if total_users_elements:
            total_users_text = total_users_elements[0].get_text(strip=True)
            total_users_match = re.search(r'(\d+,\d+|\d+)', total_users_text)
            total_users = total_users_match.group(0) if total_users_match else 'No total users found'
        else:
            total_users = 'No total users found'

        if extension_type_elements:
            extension_type = extension_type_elements[-1].get_text(strip=True)
        else:
            extension_type = 'No type found'


        # Debugging: Print extracted values
        print(f"Extension Name: {extension_name}")
        print(f"Extension URL: {extension_url}")
        print(f"Developer: {developer}")
        print(f"Overall Rating: {overall_rating}")
        print(f"Total Rating: {total_rating}")
        print(f"Extension Type: {extension_type}")
        print(f"Total Users: {total_users}")

        # Check if extension info already exists
        existing_info = supabase.table('extension_info').select('*').eq('extension_name', extension_name).execute()
        if not existing_info.data:
            # Insert data into extension_info table
            extension_info_data = {
                'extension_name': extension_name,
                'extension_url': extension_url,
                'developer': developer,
                'overall_rating': overall_rating,
                'total_rating': total_rating,
                'extension_type': extension_type,
                'total_users': total_users
            }
            extension_info_response = supabase.table('extension_info').insert(extension_info_data).execute()
            print("Extension info has been successfully stored in Supabase.")
            print(extension_info_response)
        else:
            print("Extension info already exists in the database.")

        # Ensure all lists are the same length
        length = min(len(names), len(dates), len(ratings), len(reviews), len(helpfuls))

        # Trim lists to the same length
        names = names[:length]
        dates = dates[:length]
        ratings = ratings[:length]
        reviews = reviews[:length]
        helpfuls = helpfuls[:length]

        # Prepare data for extension_review table
        extension_review_data = [
            {
                'name': names[i],
                'date': dates[i],
                'rating': ratings[i],
                'review': reviews[i],
                'helpful': helpfuls[i],
                'extension_name': extension_name
            }
            for i in range(length)
        ]

        for review in extension_review_data:
            # Check if review already exists
            existing_review = supabase.table('extension_review').select('*').eq('name', review['name']).eq('date', review['date']).eq('rating', review['rating']).eq('review', review['review']).eq('helpful', review['helpful']).eq('extension_name', review['extension_name']).execute()
            if not existing_review.data:
                # Insert data into extension_review table
                extension_review_response = supabase.table('extension_review').insert(review).execute()
                print("Review has been successfully stored in Supabase.")
                print(extension_review_response)
            else:
                print("Review already exists in the database.")

        # Clean up
        browser.close()

if __name__ == '__main__':
    main()
