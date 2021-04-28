[toc]

# ESC 프로젝트

## 게시물

### 📄 Index

#### ☝ jQuery를 이용한 게시

> 모든 게시글 => 텍스트 형태로 게시
>
> 사진이 있는 게시글 => 카드 모양으로 게시

![image-20210423214458117](%EA%B4%91%EB%A9%94/image-20210423214458117.png)![image-20210423214536546](%EA%B4%91%EB%A9%94/image-20210423214536546.png)

- index.html

  ```html
  <div>
      <button class="btn btn-white" id="text"><i class="fas fa-align-justify"></i></button>
      <button class="btn btn-white" id="image"><i class="fas fa-th-large"></i></button>
  </div>
  <div id="texts">
      ...
      모든 article 데이터들 Read 구현
      ...
  </div>
  <div id="images" style="display: none;">
      ...
      카드에 해당하는 데이터들 Read 구현
      ...
  </div>
  <script src="{% static 'js/index.js' %}"></script>
  ```

  ✔ 이미지 내용들의 `display`를 `none`으로 해서 기본값을 텍스트 형태만 보이도록 구현!

👉 목표 : jQuery를 이용하여 `#image`아이콘을 클릭하면 `#images`를 게시, 

​				`#text`아이콘을 클릭하면 `#texts`를 게시

- index.js

  ```javascript
  $(document).ready(function(){
    $("#text").click(function(){
      $("#texts").show();
      $("#images").hide();
    });
    $("#image").click(function(){
      $("#images").show();
      $("#texts").hide();
    });
  });
  ```

  ✔ jQuery의 `show`와 `hide`기능을 이용하여,

  ​	 `#text`아이콘을 클릭했을 때 `#texts`를 보여주고 `#images`를 숨김

  ​	`#image`아이콘을 클릭했을 때 `#images`를 보여주고 `#texts`를 숨김



### 📚 카테고리

#### ☝ 선택한 카테고리에 알맞은 게시물들 제시

![image-20210423223611228](%EA%B4%91%EB%A9%94/image-20210423223611228.png)

- views.py

  ```python
  @require_safe
  def board(request, category):
      articles = Article.objects.filter(category=category).order_by('-created_at')
      ...
      context = {
          'articles': articles,
          ...
      }
      return render(request, 'articles/board.html', context)
  ```

  ✔ `filter`를 이용하여 선택한 카테고리에 알맞은 게시물들을 추출

  ​	생성시간인 `created_at`의 역방향으로 `order_by`하여 최신순으로 정렬!



#### ✌ 좋아요 개수를 기반으로 Hot 게시글 제시

![image-20210423224012090](%EA%B4%91%EB%A9%94/image-20210423224012090.png)

- views.py

  ```python
  @require_safe
  def board(request, category):
      likes = Article.objects.order_by('-like_users')[:3]
      ...
      context = {
          'likes': likes,
          ...
      }
      return render(request, 'articles/board.html', context)
  ```

  ✔ `like_users`를 기준으로 역방향 `order_by`를 줘서, 좋아요 개수가 많은 순서로 정렬 후, 상위 3개만 추출



### 👀 자세히보기

#### ☝ 자신이 작성한 게시물에만 수정, 삭제 버튼 제시

![image-20210423224513755](%EA%B4%91%EB%A9%94/image-20210423224513755.png)

![image-20210423224640959](%EA%B4%91%EB%A9%94/image-20210423224640959.png)

- detail.html

  ```html
  {% if request.user == article.user %}
      <hr>
      <div class="d-flex justify-content-end mx-4">
      <a class="btn btn-success mx-1" href="{% url 'articles:update' article.pk %}" role="button">수정</a>
      <button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#exampleModal">
        삭제
      </button>
      ...
  {% endif %}
  ```

  ✔ `request.user(로그인 된 유저)`와 `article.user(게시글 작성 유저)`가 동일한 경우만 `수정`과 `취소`버튼 제시

  

### ✒ 글 작성

#### ☝ formset을 이용하여 여러개의 이미지 업로드

![image-20210423225228366](%EA%B4%91%EB%A9%94/image-20210423225228366.png)

- forms.py

  ```python
  class PhotoForm(forms.ModelForm):
      image = forms.ImageField(
          ...
      )
      class Meta:
          model = Photo
          fields = ('image',)
  
  PhotoFormSet = forms.inlineformset_factory(Article, Photo, form=PhotoForm, extra=5)
  ```

  ✔ `inlineforset_factory`를 이용하여 이미지 폼을 갖고 와 엮어서 폼셋으로 만들기

  ✔ `입력할 데이터의 부모 모델`, `데이터 입력할 모델`, `기본 폼`, `이미지 개수` 순서로 인자를 넣어준다. 

- views.py

  ```python
  from django.db import transaction
  
  @login_required
  @require_http_methods(['GET', 'POST'])
  def create(request):
      if request.method == 'POST':
          article_form = ArticleForm(request.POST)
          photo_formset = PhotoFormSet(request.POST, request.FILES)
          if article_form.is_valid() and photo_formset.is_valid():
              article = article_form.save(commit=False)
              article.user = request.user
              with transaction.atomic():
                  article.save()
                  photo_formset.instance = article
                  photo_formset.save()
                  return redirect('articles:index')
      else:
          article_form = ArticleForm()
          photo_formset = PhotoFormSet()
      context = {
          'article_form': article_form,
          'photo_formset': photo_formset,
      }
      return render(request, 'articles/create.html', context)
  ```

  ✔ `transaction`이 여러 개의 프로세스가 묶여져 하나처럼 동작할 수 있도록 해준다.

  

### ✂ 글 수정

#### ☝ 이미지 수정

![image-20210423230442631](%EA%B4%91%EB%A9%94/image-20210423230442631.png)

- update.html

  ```html
  {{ photo_form.management_form }}
      {% for form in photo_form %}
        {% for photo in photos %}
          {% if photo.id == form.instance.id %}
            <div class="mb-2">
              <p>현재 이미지{{ forloop.counter }} :</p>
              <div class="d-flex align-items-end">
                <img src="{{ photo.image.url }}" alt="" width="100px;">
                <input class="form-control" style="height: 38px;" type="text" placeholder="{{ photo.image }}" aria-label="Disabled input example" disabled>
              </div>              
            </div>
            <fieldset class="aligned">
              <div class="form-row">
                {% comment %} <p>변경:</p> {% endcomment %}
                {{ form.image }}
              </div>
            </fieldset>
            <br>
          {% endif %}
        {% endfor %}      
      {% endfor %}    
  ```

  ✔ 폼셋에 들어있는 각 폼을 다루는 경우, `{{ photo_formset.management_form }}` 반드시 추가해야 함‼ 

  ​	(=> 글 작성에서도 마찬가지!)

  ✔ `for`과 `if`를 사용하여, `수정하고 싶은 현재 이미지`와 `수정할 이미지 업로드 폼`을 짝지어준다.

  

### 🗑 글 삭제

#### ☝ 글을 삭제하기 전에 모달로 확인

> `bootstrap`을 이용하여 모달 제시

![image-20210423231035162](%EA%B4%91%EB%A9%94/image-20210423231035162.png)

- detail.html

  ```html
  <button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#exampleModal">
        삭제
  </button>
  
  {% comment %} 모달 {% endcomment %}
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body text-center">
              <h5 class="fw-bold">정말 삭제하시겠습니까?</h5>
            </div>
            <div class="modal-footer">
              <form action="{% url 'articles:delete' article.pk %}" mehtod="POST">
                {% csrf_token %}
                <button class="btn btn-primary">Yes</button>
              </form>            
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  ```

  ✔ 삭제 버튼에 `data-bs-toggle="modal"`와 `data-bs-target="#exampleModal"`를 주어 버튼 클릭했을 때, `#exampleModal`모달이 열리도록 하자

  ✔ 모달의 id를 `exampleModal`로 해서 모달의 주인공으로 만들기

  ✔ 모달의 Yes 버튼은 POST 방식으로 삭제 함수 작동

  ✔ 모달의 No 버튼은 `data-bs-dismiss="modal"`을 줘서 모달 닫기



### 🔍 글 검색

#### ☝ 검색 결과 제시

> 제목에 검색어가 포함되어 있는 게시글 제시 

![image-20210423232015105](%EA%B4%91%EB%A9%94/image-20210423232015105.png)

>제목에 검색어가 포함되어 있지 않은 경우의 화면

![image-20210423232037779](%EA%B4%91%EB%A9%94/image-20210423232037779.png)

- views.py

  ```python
  @require_POST
  def search(request):
      articles = Article.objects.order_by("-created_at")
      search = request.POST.get('search')
      search_articles = []
      for article in articles:
          if search in article.title:
              search_articles.append(article)
      context = {
          'articles': articles,
          'search': search,
          'search_articles': search_articles,
      }
      return render(request, 'articles/search.html', context)
  ```

  ✔ 게시글의 제목에 입력한 검색어가 포함되면, 그 게시글들을 `search_articles`리스트에  추가

- search.html

  ```html
  {% if search_articles %}
  <div class="text-center my-5">
  	...
      입력한 검색어가 포함된 제목의 게시글들 제시하는 코드
      ...
  </div>
  {% else %}
  <div class="text-center my-5">
      <h3 class="fw-bold" style="display: inline; color: green;">'{{ search }}'</h3>
      <h3 style="display: inline;">에 대한 검색 결과가 존재하지 않습니다.</h3>
  </div>
  {% endif %}
  ```

  ✔ `if`를 이용하여 검색 결과에 대한 상황과 내용 알려주기

  

## 댓글

### 💬 댓글 수정 ⭐⭐⭐⭐⭐

#### ☝ 댓글 수정 폼 제시 & 숨기기

> javaScript를 이용하여 `수정`버튼을 누르면 수정 폼 제시
>
> 수정 폼이 제시된 상태에서 `수정`버튼이나 `수정 취소`버튼을 누르면 수정 폼 숨기기

![image-20210423233838025](%EA%B4%91%EB%A9%94/image-20210423233838025.png)

- detail.html

  ```html
  <button class="btn btn-white mx-1 commentUpdateCancelBtn" id="commentUpdateCancel{{ comment.id }}" data-id={{ comment.id }} style="display: none;">수정</button>
  
  <div id="commentUpdateForm{{ comment.id }}" style="display: none;">
        <form action="{% url 'articles:comment_update' article.pk comment.pk %}" method="POST">
          {% csrf_token %}
          <div class="d-flex justify-content-center">
            {% for comment_update_form in comment_update_forms %}
              {% if comment.id == comment_update_form.instance.id %}
                {{ comment_update_form.content }}
              {% endif %}
            {% endfor %}                  
          </div>
          <br>
          <div class="d-flex justify-content-end mx-4">
            <button type="submit" class="btn btn-warning btn-sm mx-1">수정 완료</button>
            <button type="button" class="btn btn-secondary btn-sm mx-1 commentUpdateCancelBtn" id="commentUpdateCancel{{ comment.id }}" data-id={{ comment.id }}>수정 취소</button>
          </div>
      </form>
  </div> 
  <script src="{% static 'js/comment.js' %}"></script>
  ```

  ✔ 댓글 수정 폼은 스타일의 기본값으로 `display: none`을 설정하여 아무 행동도 안 했을 경우 댓글 수정 폼이 안 보이도록 해준다.

  ✔ JavaScript에서 이용할 수 있도록 각 `id`이름에 댓글의 고유한 값인`comment.id`를 포함시켜 지어준다.

  ✔ `수정 버튼`과 `수정 취소 버튼`에는 새로운 class 를 줘서 JavaScript에서 사용할 수 있도록 준비!

  ​	수정 버튼 :  `commentUpdateCancelBtn`

  ​	수정 취소 버튼 : `commentUpdateCancelBtn`

  ✔ 수정 버튼의 토글 기능을 위해, 2개의 수정 버튼을 만들어준다.

  ​	👉 1개는 수정 버튼 class : commentUpdateCancelBtn`

  ​		  나머지 1개는 수정 취소 버튼 class : `commentUpdateCancelBtn`

  ✔ Script에서 `comment.id`를 이용할 수 있도록,`수정 버튼`과 `수정 취소 버튼`에 `data-id={{ comment.id }}`를 입력해 준다.

- comment.js

  ```javascript
  // 1. 모든 수정 버튼을 갖고온다.
  const updateBtns = document.querySelectorAll('.commentUpdateBtn')
  // ['1번 댓글 수정버튼', '2번 ...', '3번 ...', ...]
  
  // 2. 모든 수정 버튼에 "클릭 이벤트를 단다."
  updateBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // 3. 기존의 내용을 지우고,
      document.querySelector(`#commentContent${btn.dataset.id}`).style.display = "none";
      // 4. 수정 form을 보여준다.
      document.querySelector(`#commentUpdateForm${btn.dataset.id}`).style.display = "block";
      // 수정, 수정 취소 토글
      document.querySelector(`#commentUpdate${btn.dataset.id}`).style.display = "none";
      document.querySelector(`#commentUpdateCancel${btn.dataset.id}`).style.display = "block";
    })
  })
  ```

  ✔  수정 버튼을 누르면 `기존 내용 숨기기기`와 `수정 폼 보여주기`를 할 수 있도록`style`의 `display`값을 변경시켜준다.

  ✔ Html에서 받아온 `data-id={{ comment.id }}`값은 `_.dataset.id`로 사용될 수 있다.

  ​	👉 즉, 여기에서는 `btn.dataset.id`로 사용되었다.

  ✔ Script에서 `data-id`값을 사용하기 위해, `$`와 `{}`를 이용한다.

  ​	👉 여기에서는 `#commentContent${btn.dataset.id}`로 사용되었다.

  ```javascript
  const updateCancelBtns = document.querySelectorAll('.commentUpdateCancelBtn')
  
  updateCancelBtns.forEach(cancelBtn => {
    cancelBtn.addEventListener('click', () => {
      document.querySelector(`#commentUpdateForm${cancelBtn.dataset.id}`).style.display = "none";
      document.querySelector(`#commentContent${cancelBtn.dataset.id}`).style.display = "block";
      // 수정, 수정 취소 토글
      document.querySelector(`#commentUpdateCancel${cancelBtn.dataset.id}`).style.display = "none";
      document.querySelector(`#commentUpdate${cancelBtn.dataset.id}`).style.display = "block";    
    })
  })
  ```

  ✔ 수정 취소 버튼이나 수정 버튼을 누르면 `기존 내용 보여주기`와 `수정 폼 숨기기`를 할 수 있도록`style`의 `display`값을 변경시켜준다.



#### ✌ 댓글 폼 안에 현재 댓글 내용 제시

- views.py

  ```python
  @require_safe
  def detail(request, article_pk):
      ...
      comments = article.comment_set.order_by('-created_at')
      comment_update_forms = []
      for comment in comments:
          comment_update_forms.append(CommentForm(instance=comment))
      context = {
          ...
          'comments': comments,
          "comment_update_forms": comment_update_forms,
      }
      return render(request, 'articles/detail.html', context)
  ```

  ✔ `댓글 폼`의 instance에 댓글의 내용들을 입력하여,

  ​	`comment_update_forms`리스트에 넣어주고 댓글 폼에 나타내줄 수 있도록 한다.

  