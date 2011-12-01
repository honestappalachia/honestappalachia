from django.db import models

from templatetags.wiki import wikify

# Create your models here.
class Page(models.Model):
    '''
    A Wiki article
    '''
    name = models.CharField(max_length=100)
    content = models.TextField()
    rendered = models.TextField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def render(self):
        '''
        Renders body into body_html, as Markdown for now
        Escapes any HTML added by the user.
        Converts any WikiWords into links
        '''
        import markdown
        md = markdown.Markdown(
                extensions=['toc'],
                extension_configs={
                    'toc': [
                        ('anchorlink', True),
                    ],
                },
                safe_mode="escape",
            )
        content_md = md.convert(self.content)
        self.rendered= wikify(content_md)

    def preprocess(self):
        '''
        Renders content into rendered
        '''
        self.render()

    def save(self, *args, **kwargs):
        '''
        Override save to add preprocessing
        '''
        self.preprocess()
        super(Page, self).save(*args, **kwargs)
