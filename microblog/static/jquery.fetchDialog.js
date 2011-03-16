(function($){
	$.fn.fetchDialog = function(options) {
		var defaults = { 
			enter: function(){},
			exit: function(){}
		};
		var opts = $.extend(defaults, options);
		if($("#UrlFetcherWrap").length <= 0){
			var url_fetcher=$("<div id='UrlFetcherWrap' class='box-shadow gradient-sliver'><div id='UrlFetcher'><input type='text' name='urlfetcher' /><button id='Fetchbtn' class='button orange'>我要备份</button></div></div>");
			$('body').append(url_fetcher);
			url_fetcher.append("<div class='fetcher-close-dialog'></div>");
		}else{
			var url_fetcher = $("#UrlFetcherWrap");
		}
		
		return this.each(function(){

			opts.click_flag=0;
			$(this).bind('click',function(){
				showDialog();
			});
			$('.fetcher-close-dialog').bind('click', function(){
				hideDialog();
			});
			function showDialog(){
				url_fetcher.fadeIn();
			}
			function hideDialog(){
				url_fetcher.fadeOut();
			}
			$('#Fetchbtn').click(function(){
				var url=$(this).prev().val();
				$.ajax({
					type:'POST',
					url:'/api/submit',
					data:url,
					async:false,
					timeout: 3000,
					error: function(msg){
						hideDialog()
					},
					success: function(msg){
						hideDialog()
					}
				});
			});
		})
	}
})(jQuery);
