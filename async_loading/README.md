# Asynchronous content loading

This *recipe* adds a (very basic) Javascript helper function to load HTML tag contents asynchronously on page loada. This is useful in cases where a lot of information needs to be displayed and the page load time can be severly affected.

In order to use the function, define a base tag such as:

```html
<div class="container async-load" data-loader="<MY_URL>">
    <h1>This content will be replaced</h1>
</div>
```

**NOTE**: you can build the URL defined in the `data-loader` attribute using the `url_for` Jinja function.

When the page is loaded, the Javascript function will be applied to all elements that have the `.async-load` class, performing an AJAX request to the URL defined by their `data-loader` attribute and **replacing** the contents (in this case, the `<h1>` tag) with the response from the server.

For instance, you could return a partial view of an HTML table or charts to display in the page.
