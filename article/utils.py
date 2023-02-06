from django.utils.datastructures import MultiValueDictKeyError

def _checker(value):
    try:
        if value['like'] == "likebutton":
            return "like"
        elif value['like'] == "dislikebutton":
            return "dislike"
            # return render(request, "blog/blog_detail.html", {"likes":like_obj})
    except MultiValueDictKeyError:
        return "Error"