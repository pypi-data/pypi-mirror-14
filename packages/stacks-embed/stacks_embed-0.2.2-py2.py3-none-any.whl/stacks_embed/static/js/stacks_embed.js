var StacksEmbed = function(){

};

StacksEmbed.prototype.init = function(){
    $('.js-embed-placeholder').on('click', function(){
        var that = $(this);
        var embedCode = that.data('embed-code');
        var embedCodeProcessed = embedCode.replace(
            "__WIDTH__",
            that.width() + 'px'
        ).replace(
            "__HEIGHT__",
            that.height() + 'px'
        )
        that.html(embedCodeProcessed);
    });
};

module.exports = StacksEmbed;
