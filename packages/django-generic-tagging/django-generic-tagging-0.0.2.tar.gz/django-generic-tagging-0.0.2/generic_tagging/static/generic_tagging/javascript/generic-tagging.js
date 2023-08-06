$(function() {
    'use strict'
    var $containers = $(".generic-tagging-container");
    $containers.each(function() {
        var $tagList = $(this).find('.tag-list');
        var $tagTemplate = $(this).find('.tag');
        var objectID = $(this).data('object-id');
        var contentType = $(this).data('content-type');

        $tagTemplate.remove();
        var $list = $(this).find('.tag-list');
        var listAPIEndpoint = $list.data('tag-list-api');

        function addTag(item, animation) {
            var $newTag = $tagTemplate.clone();
            var $link = $newTag.find('a.tag-link');
            $link.text(item['tag']['label']);
            $link.attr('href', item['tag']['url']);
            $tagList.append($newTag);

            $newTag.find('.delete-button').attr('href', item['detail_api_url']);
            var $lockLink = $newTag.find('.lock-button');
            $lockLink.attr('href', item['lock_api_url']);

            var $unlockLink = $newTag.find('.unlock-button');
            $unlockLink.attr('href', item['unlock_api_url']);
            toggleLockState($newTag, item['locked']);

            if (animation) {
                $newTag.fadeOut(0);
                $newTag.fadeIn('slow');
            }
        }

        function toggleLockState($tag, locked) {
            var $deleteLink = $tag.find('.delete-button');
            var $lockLink = $tag.find('.lock-button');
            var $unlockLink = $tag.find('.unlock-button');
            if (locked) {
                $lockLink.hide();
                $unlockLink.show();
                $deleteLink.hide();
                $tag.addClass('locked');
            } else {
                $lockLink.show();
                $deleteLink.show();
                $unlockLink.hide();
                $tag.removeClass('locked');
            }
        }

        // form
        var $addTagButton = $(this).find('.add-tag-button');
        var $addTagForm = $(this).find('.add-tag-form');
        $addTagForm.hide();
        $addTagButton.on('click', function(e) {
            e.preventDefault();
            if ($(this).hasClass("active")) {
                $(this).removeClass("active");
                $addTagForm.hide();
            } else {
                $(this).addClass("active");
                $addTagForm.show();
                $addTagForm.find("input[type='text']").focus();
            }
        });

        // retrieve
        $.when($.get(listAPIEndpoint, {'object_id': objectID, 'content_type': contentType}))
            .done(function(tags) {
                tags.forEach(function(item) {
                    addTag(item);
                });
            })
            .fail(function(e) {
                alert(e['responseJSON']);
            });

        // create
        $addTagForm.on('submit', function(e) {
            e.preventDefault();
            var endpoint = $(this).attr('action');
            var params = $(this).serializeArray();
            $.when($.post(endpoint, params))
                .done(function(item) {
                    $addTagForm.find('.label-input').val('');
                    addTag(item, true);
                })
                .fail(function(e) {
                    alert(e['responseJSON']);
                });
           return false;
        });

        //delete
        $tagList.delegate('.delete-button',
            'click',
            function(e) {
                e.preventDefault();
                if (confirm("Are you sure to delete this tag?")) {
                    var $tag = $(this).closest('li.tag');
                    var deleteEndPoint = $(this).attr('href');
                    $.when($.ajax({'method': 'DELETE', 'url': deleteEndPoint}))
                        .done(function(response) {
                            $tag.fadeOut('slow', function() {
                                $(this).remove();
                            });
                        })
                        .fail(function(response) {
                            alert(response['responseJSON']);
                        });
                }
                return false;
        });

        // lock
        $tagList.delegate('.lock-button', 'click', function(e) {
            e.preventDefault();
            var $tag = $(this).closest('li.tag');
            var lockEndPoint = $(this).attr('href');
            $.when($.ajax({'method': 'PATCH', 'url': lockEndPoint}))
                        .done(function(response) {
                            toggleLockState($tag, true);
                        })
                        .fail(function(response) {
                            alert(response['responseJSON']);
                        });
        });

        // unlock
        $tagList.delegate('.unlock-button', 'click', function(e) {
            e.preventDefault();
            var $tag = $(this).closest('li.tag');
            var unlockEndPoint = $(this).attr('href');
            $.when($.ajax({'method': 'PATCH', 'url': unlockEndPoint}))
                        .done(function(response) {
                            toggleLockState($tag, false);
                        })
                        .fail(function(response) {
                            alert(response['responseJSON']);
                        });
        });
    });
});
