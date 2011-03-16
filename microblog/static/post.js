$(function(){
	$('html').ajaxSend(function(event, xhr, settings) {
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			// Only send the token to relative URLs i.e. locally.
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		}
	});


	$('#FollowBtn').click(function(){
		var followText = $(this)
		$.ajax({
			type: 'POST',
			url: '/follow/',
			data: $(this).val(),
			error: function(msg){alert('Fail')},
			success: function(msg){
				followText.text(msg)
				if(followText.hasClass('orange')){
					followText.removeClass('orange')
					followText.addClass('green')
					followText.text('已关注')
				}else if(followText.hasClass('green')){
					followText.removeClass('green')
					followText.addClass('orange')
					followText.text('关注')
				}
			}
		});
	})



	$('.conversation .topic-reply').click(function(){
		var topic =$(this).parent().parent().parent().parent().parent().parent()
		topic.find('.conversation-form').toggle();
	});

	$('.conversation .favbtn').click(function(){
		var data = {'id':$(this).val()}
		var fav_icon = $(this)
		$.ajax({
			type: 'POST',
			url: '/fav/',
			data: data,
			error: function(msg){alert(msg.responseText)},
			success: function(msg){
				if(fav_icon.hasClass('fav')){
					fav_icon.removeClass('fav')
					fav_icon.addClass('unfav')
				}else {
					fav_icon.removeClass('unfav')
					fav_icon.addClass('fav')
				}
			}
		});
	});


	$('.conversation .topic-delete').click(function(){
		var topic =$(this).parent().parent().parent().parent().parent().parent()
		var data = {'id':$(this).val()}
		$.ajax({
			type: 'POST',
			url: '/delete/',
			data: data,
			error: function(msg){alert('Fail')},
			success: function(msg){
				topic.hide();
			}
		});
	});

	$('.conversation-form .closebtn').click(function(){
		var topic =$(this).parent()
		topic.toggle();
	});

	$('.topic-content-wrap .conversation-form .conversation-button').click(function(){
		var content = $(this).parent().find('input[name=conversation]').val()
		var authorprotrait = $('#UserProprait').html()
		var conversation_json = {'id':$(this).parent().find('input[name=topic-id]').val(),'content':$(this).parent().find('input[name=conversation]').val()}
		var conversation_form = $(this).parent()
		var authorname = $('#AuthorName').text()
		if(conversation_json.content.length>0&&conversation_json.content.length<200){
			$.ajax({
				type: 'POST',
				url: '/conversation/',
				data: conversation_json,
				error: function(msg){alert('Fail')},
				success: function(msg){
				conversation_form.find('input[name=conversation]').val('');
				conversation_form.toggle();
				$('#TopicWrap').prepend("<div class='topic-all even'><div class='topic-left'><div class='topic-author'><div class='topic-author-protrait'>"+authorprotrait+"</div><div class='topic-author-nickname'>"+authorname+"</div></div></div><div class='topic-right'><div class='topic-meta'><span class='topic-datetime'></span></div><div class='topic-content-wrap'><div class='topic-content'>"+msg+"</div></div></div><div class='clearfix'></div></div>");
				$('html, body').animate({scrollTop: '0px'}, 800);
				}
			});
		}else{
			alert('您输入的字符长度有误！'+conversation_json.content.length);
		}
	});


	$('#TopicButton').click(function(){
		var content = $('#TopicForm').val()
		var authorname = $('#AuthorName').text()
		var authorprotrait = $('#UserProprait').html()
		if(content.length>0&&content.length<200){
			$.ajax({
			type: 'POST',
			url: '/post/',
			data: content,
			async: false,
			error: function(msg){alert('Fail')},
			success:  function(msg){
			$('#TopicWrap').prepend("<div class='topic-all even'><div class='topic-left'><div class='topic-author'><div class='topic-author-protrait'>"+authorprotrait+"</div><div class='topic-author-nickname'>"+authorname+"</div></div></div><div class='topic-right'><div class='topic-meta'><span class='topic-datetime'></span></div><div class='topic-content-wrap'><div class='topic-content'>"+msg+"</div></div></div><div class='clearfix'></div></div>");
			$('#TopicForm').val('');
			}
			});
		}else{
			alert('您输入的字符长度有误！'+content.length);
		}
	});
})

