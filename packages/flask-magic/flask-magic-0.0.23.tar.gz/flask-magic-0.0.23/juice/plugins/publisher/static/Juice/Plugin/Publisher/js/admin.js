var WPMDEditor;

$(function(){
// Categories and Types

    var modalCatType = $("#modal-cat-type")
    modalCatType.on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var modal = $(this)
        var nameEl = modal.find(".modal-body [name='name']")
        var slugEl = modal.find(".modal-body [name='slug']")
        var delButton = modal.find("button.delete-btn")

        if (button.data("id") == "") {
            delButton.hide()
        } else {
            delButton.show()
        }
        slugEl.slugify(nameEl)
        modal.find("input[name='action']").val("update")
        modal.find("[name='id']").val(button.data("id"))
        nameEl.val(button.data("name"))
        slugEl.val(button.data("slug"))
    })
    modalCatType.find("button.delete-btn").click(function(){
        if(confirm("Do you want to DELETE this ?")) {
            modalCatType.find("input[name='action']").val("delete")
            modalCatType.find("form").submit()
        }
    })


// EDIT
    var formPostEdit = $("#form-post-edit");
    if (formPostEdit.length > 0) {
        var titleInput = formPostEdit.find("[name='title']")
        var statusInput = formPostEdit.find("[name='status']")
        var postType = formPostEdit.find("[name='type_id']")
        var contentInput = formPostEdit.find("[name='content']")
        var slugInput = formPostEdit.find("[name='slug']").first()
        var postTags = formPostEdit.find("[name='tags']").first()

    //--- Slug
        slugInput.slugify(titleInput)

    //--- Tags
        postTags.tokenfield({showAutocompleteOnFocus: true})

        // Unique tags
        postTags.on('tokenfield:createtoken', function (event) {
            var existingTokens = $(this).tokenfield('getTokens');
            $.each(existingTokens, function(index, token) {
                if (token.value === event.attrs.value)
                    event.preventDefault();
            });
        });

    //---
        $(".action-btn").click(function(){
            var el = $(this)
            var action = el.data("action")

            if (action == "draft" || action == "publish") {
                if (titleInput.val().trim() == "") {
                    alert("Your Post Title is missing")
                } else if (! postType.is(":checked")) {
                    alert("You need to select a post type")
                } else {
                    statusInput.val(action)
                    formPostEdit.submit()
                }

            } else if (action == "delete") {
                if (confirm("Do you really want to delete this post ?")) {
                    statusInput.val("delete")
                    formPostEdit.submit()
                }
            }
        })

        //-- Inline Category in Post Edit
        var modalCatInline = $("#modal-insert-cat-inline")
        var modalCatInlineForm = modalCatInline.find("form").first()

        modalCatInline.on("click", ".save-button", function(){
            $.post(modalCatInlineForm.attr("action"), modalCatInlineForm.serialize(), function(data){
                if (data.status == "OK") {

                    var label = $("<label />", {text: data.name})
                    var field = $("<input />", {type: "checkbox",
                                                name: "post_categories",
                                                value: data.id,
                                                checked: "checked"})
                    $("<div />", {"class": "checkbox-group"})
                        .append(field)
                        .append(label)
                        .appendTo($(".post-categories-list"))
                } else {
                    alert("Couldn't save the category. It probably exists already")
                }
            }, "json")
            modalCatInline.modal('hide')
        })
    }

// IMAGES

    //-- Category and Type admin
    var modalImg = $("#modal-edit-image")
    modalImg.on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var modal = $(this)
        modal.find("input[name='action']").val("update")
        modal.find("[name='id']").val(button.data("id"))
        modal.find(".modal-body [name='description']").val(button.data("description"))
        modal.find("img#modal-image-preview").attr("src", button.data("object_url"))
        modal.find(".modal-body [name='object_url']").val(button.data("object_url"))
    })
    modalImg.find("button.delete-btn").click(function(){
        if(confirm("Do you want to DELETE this image ?\n It will no longer exist")) {
            modalImg.find("input[name='action']").val("delete")
            modalImg.find("form").submit()
        }
    })

// SORTABLE TABLE ROWS

    $('.sorted_table').sortable({
        containerSelector: 'table',
        itemPath: '> tbody',
        itemSelector: 'tr',
        placeholder: '<tr class="placeholder"/>'
    });


// FEATURED IMAGE. It uses the MDEditor image_browser to access the images
    var featImgInputEl = $("#featured-image-input")
    var featImgEl = $(".featured-image-container img")
    featImgInputEl.on('change', function() {
         featImgEl.prop('src', this.value);
    })
    $("#btn-select-featured-image").click(function(){
        WPMDEditor.image_browser(function(url){
            featImgInputEl.val(url)
            featImgEl.prop("src", url)
        })

    })

// FEATURED EMBED, for Oembed content
    var featEmbedInputEl = $("#featured-embed-input")
    var featEmbedPreview = $("#featured-embed-preview")
    featEmbedInputEl.on('change', function() {
         featEmbedPreview.empty()
         featEmbedPreview.append($("<a>",{"href": this.value, "class": "oembed"}))
         $("a.oembed").oembed()
    })


})

