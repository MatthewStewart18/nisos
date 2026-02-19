import requests
from typing import TypedDict

class Profile(TypedDict):
    biography: str
    full_name: str
    is_verified: bool
    profile_pic_url: str
    username: str
    posts: list[dict]

# fetch, parse and return profile object
def get_social_media_profile(url: str) -> Profile:

    response = requests.get(url)
    data = response.json()

    biography = data.get('graphql').get('user').get('biography')
    full_name = data.get('graphql').get('user').get('full_name')
    is_verified = data.get('graphql').get('user').get('is_verified')
    profile_pic_url = data.get('graphql').get('user').get('profile_pic_url')
    username = data.get('graphql').get('user').get('username')
    posts = data.get('graphql').get('user').get('timeline_media').get('posts')

    profile: Profile = {
        "biography": biography,
        "full_name": full_name,
        "is_verified": is_verified,
        "profile_pic_url": profile_pic_url,
        "username": username,
        "posts": posts
    }

    return profile