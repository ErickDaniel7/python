import secrets
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_and_savelinks(file_name, num_links):
    with open(file_name, 'a') as file:
        for _ in range(num_links): # 342 LOL
            random_string = generate_random_string(342)
            url = f"https://discord.com/billing/partner-promotions/1180231712274387115/eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..{random_string}\n"
            file.write(url)

# the input
num_links = int(input("Enter the number of links to generate: "))

# saves here btw
generate_and_savelinks('links.txt', num_links)

print(f"{num_links} link(s) generated and saved to 'links.txt'.")
