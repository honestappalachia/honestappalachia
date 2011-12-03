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
    toc = models.TextField(editable=False)
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
        from toc import genTOC, header_permalinks

        # render self.content as Markdown
        md = markdown.Markdown(
                safe_mode="escape",
            )
        rend = md.convert(self.content)
        # generate TOC
        self.toc = genTOC(rend)
        # convert headers to permalinks
        rend = header_permalinks(rend)
        # convert WikiWords to links, save in self.rendered
        self.rendered = wikify(rend)

    def save(self, *args, **kwargs):
        '''
        Override save to add preprocessing
        '''
        self.render()
        super(Page, self).save(*args, **kwargs)
