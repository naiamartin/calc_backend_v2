from pydantic import BaseModel, ConfigDict


class BlogBase(BaseModel):
    title: str
    text: str


# Schema for creating a new blog
class BlogCreate(BlogBase):
    pass


class BlogUpdate(BlogBase):
    title: str | None = None
    text: str | None = None


# Schema for reading/returning a blog(includes id)
class Blog(BlogBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
