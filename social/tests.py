import json
from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from config.schema import schema
from .models import Post

User = get_user_model()

class SocialTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.post = Post.objects.create(author=self.user, content="Initial Post")

    def test_create_post_mutation(self):

        
        self.client.force_login(self.user)
        
        query = '''
            mutation {
                createPost(content: "New Test Post") {
                    post {
                        content
                        author {
                            username
                        }
                    }
                }
            }
        '''
        response = self.client.post('/graphql/', data={'query': query}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertNotIn('errors', content)
        self.assertEqual(content['data']['createPost']['post']['content'], "New Test Post")

    def test_create_comment_mutation(self):
        self.client.force_login(self.user)
        

        from graphql_relay import to_global_id
        post_global_id = to_global_id("PostType", self.post.id)

        query = f'''
            mutation {{
                createComment(postId: "{post_global_id}", text: "Nice post!") {{
                    comment {{
                        text
                        post {{
                            content
                        }}
                    }}
                }}
            }}
        '''
        response = self.client.post('/graphql/', data={'query': query}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertNotIn('errors', content)
        self.assertEqual(content['data']['createComment']['comment']['text'], "Nice post!")

    def test_like_post_mutation(self):
        self.client.force_login(self.user)
        from graphql_relay import to_global_id
        post_global_id = to_global_id("PostType", self.post.id)

        query = f'''
            mutation {{
                likePost(postId: "{post_global_id}") {{
                    like {{
                        user {{
                            username
                        }}
                    }}
                }}
            }}
        '''
        response = self.client.post('/graphql/', data={'query': query}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertNotIn('errors', content)
        self.assertEqual(content['data']['likePost']['like']['user']['username'], "testuser")
