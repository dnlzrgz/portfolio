from wagtail import blocks


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("CSS", "css"),
            ("Go", "Golang"),
            ("HTML", "html"),
            ("JavaScript", "js"),
            ("Python", "py"),
            ("SQL", "sql"),
        ]
    )
    code = blocks.TextBlock()

    class Meta:
        icon = "code"
        template = "blocks/code.html"
