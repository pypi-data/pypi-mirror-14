/*jsl:declare Ext*/

/**
 * Uploader implementation - with the Connection object in ExtJS 4
 *
 */
Ext.define('MP.upload.ExtJsUploader', {
    extend : 'MP.upload.AbstractUploader',

    requires : [
        'MP.upload.Connection'
    ],

    /**
     * @property
     *
     * The connection object.
     */
    conn : null,

    /**
     * @private
     *
     * Initializes and returns the connection object.
     *
     * @return {MP.upload.data.Connection}
     */
    initConnection : function() {
        var url = this.url;
        if (this.params) {
            url = Ext.urlAppend(url, Ext.urlEncode(this.params));
        }

        var conn = Ext.create('MP.upload.Connection', {
            disableCaching : true,
            method : this.method,
            url : url,
            timeout : this.timeout,
            defaultHeaders : {
                'Content-Type' : this.contentType,
                'X-Requested-With' : 'XMLHttpRequest'
            }
        });

        return conn;
    },

    /**
     * Implements {@link MP.upload.AbstractUploader#uploadItem}
     *
     * @param {MP.upload.Item} item
     */
    uploadItem : function(item) {
        var file = item.getFileApiObject();
        if (!file) {
            return;
        }

        item.setUploading();

        this.conn = this.initConnection();

        this.conn.request({
            scope : this,
            headers : this.initHeaders(item),
            xmlData : file,

            success : Ext.Function.bind(this.onUploadSuccess, this, [
                    item
                ], true),
            failure : Ext.Function.bind(this.onUploadFailure, this, [
                    item
                ], true),
            progress : Ext.Function.bind(this.onUploadProgress, this, [
                    item
                ], true)
        });
    },

    /**
     * Implements {@link MP.upload.AbstractUploader#abortUpload}
     */
    abortUpload : function() {
        if (this.conn) {
            this.conn.abort();
        }
    },

    onUploadSuccess : function(response, options, item) {
        //jsl:unused options
        var info = {
            success : false,
            message : 'general error',
            response : response
        };

        if (response.responseText) {
            var responseJson = Ext.decode(response.responseText);
            if (responseJson && responseJson.success) {
                Ext.apply(info, {
                    success : responseJson.success,
                    message : responseJson.message
                });

                this.fireEvent('uploadsuccess', item, info);
                return;
            }

            Ext.apply(info, {
                message : responseJson.message
            });
        }

        this.fireEvent('uploadfailure', item, info);
    },

    onUploadFailure : function(response, options, item) {
        //jsl:unused options
        var info = {
            success : false,
            message : 'http error',
            response : response
        };

        this.fireEvent('uploadfailure', item, info);
    },

    onUploadProgress : function(event, item) {
        this.fireEvent('uploadprogress', item, event);
    }
});
