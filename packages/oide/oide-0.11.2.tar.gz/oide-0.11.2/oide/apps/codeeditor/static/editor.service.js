'use strict';

/**
 * @ngdoc service
 * @name oide.EditorService
 * @description
 * # EditorService
 * Service to manage documents in the OIDE Editor.
 */
angular.module('oide.editor')

.factory('EditorService', ['$window', '$http', '$log', 'AceModeService', function ($window, $http,$log,AceModeService) {
  var editor = {};

  // clipboard will hold all copy/paste text for editor
  var clipboard = '';
  /**
   * This is the object from which all values concerning open documents are derived.
   * This objects has the following format:
   * {
   *   '<filepath>': {
   *     filename: str,
   *     unsaved: boolean,
   *     active: boolean,
   *     session: obj (defined by Ace)
   *   },
   *   ...
   * }
   */
  var openDocs = {};
  var editorSettings = {
    showInvisibles: true,
    useSoftTabs: true,
    fontSize: 12,
    tabSize: 4,
    showIndentGuides: true
  };

  var applySettings = function () {
    editor.setShowInvisibles(editorSettings.showInvisibles);
    editor.getSession().setUseSoftTabs(editorSettings.useSoftTabs);
    editor.setFontSize(editorSettings.fontSize);
    editor.getSession().setTabSize(editorSettings.tabSize);
    editor.setDisplayIndentGuides(editorSettings.showIndentGuides);
  };

  // Called when the contents of the current session have changed. Bound directly to
  // an EditSession.
  var onSessionModified = function(e) {
    var filepath = getCurrentDoc();
    openDocs[filepath].unsaved = true;
  };

  // Given a filepath, this function will return a filename
  var getFilenameFromPath = function(filepath) {
    var filename = filepath.substring(
      filepath.lastIndexOf('/')+1,
      filepath.length
    );
    return filename;
  };

  // Returns the next available filepath enumeration for untitled documents
  var getNextUntitledFilepath = function() {
    var docExists = true;
    var docEnum = 0;
    var filepath;
    while (docExists) {
      filepath = '-/untitled'+docEnum;
      if (filepath in openDocs) {
        docEnum++;
      } else {
        docExists = false;
      }
    }
    return filepath;
  };

  // Return the filepath of the active document in the editor. If no document
  // is active, return undefined.
  var getCurrentDoc = function() {
    var current;
    for (var filepath in openDocs) {
      if (openDocs.hasOwnProperty(filepath)) {
        if (openDocs[filepath].active) {
          current = filepath;
        }
      }
    }
    return current;
  };

  // Creates a new untitled document, which is added to openDocs
  var createUntitledDocument = function() {
    var filepath = getNextUntitledFilepath();
    createNewSession(filepath);
    switchSession(filepath);
  };

  // Make the document specified by filepath the active document in the editor.
  // Returns true if successful, and false if the specified document is not loaded.
  var switchSession = function(filepath) {
    var current = getCurrentDoc();

    if (filepath in openDocs) {
      if (current) {
        openDocs[current].active = false;
      }
      editor.setSession(openDocs[filepath].session);
      openDocs[filepath].active = true;
      // editor.setMode(openDocs[filepath].$modeId);
      applySettings();
    } else {
      return false;
    }
  };

  // Creates a new EditSession, and stores a new openDoc object in openDocs.
  // content and mode are optional.
  // This function does not set the new session as active.
  var createNewSession = function(filepath,content,mode,undoManager) {
    var c = content || '';
    var m = mode || 'ace/mode/text';
    var um = undoManager || undefined;

    openDocs[filepath] = {
      filepath: filepath,
      filename: getFilenameFromPath(filepath),
      unsaved: false,
      active: false
    };
    openDocs[filepath].session = new $window.ace.createEditSession(c,m);
    openDocs[filepath].session.on('change',onSessionModified);
    if (um) {
      openDocs[filepath].session.setUndoManager(um);
    }
  };

  return {
    /**
     * Called when ace editor has loaded. Must be bound to directive by controller.
     */
    onAceLoad: function(_ace) {
      var um,content,mode,activeSession,sel,unsaved;
      editor = _ace;
      if (Object.keys(openDocs).length !== 0) {
        for (var filepath in openDocs) {
          if (openDocs.hasOwnProperty(filepath)) {
            if (openDocs[filepath].active) {
              activeSession = filepath;
            }
            // Preserve select portions of the old EditSession, and then
            // reapply them to a new EditSession created against the editor.
            um = openDocs[filepath].session.getUndoManager();
            content = openDocs[filepath].session.getDocument();
            mode = openDocs[filepath].session.$modeId;
            sel = openDocs[filepath].session.selection;
            unsaved = openDocs[filepath].unsaved;
            createNewSession(filepath,content,mode,um);
            openDocs[filepath].session.selection = sel;
            openDocs[filepath].unsaved = unsaved;
          }
        }
        switchSession(activeSession);
      } else {
        createUntitledDocument();
      }
      applySettings();
    },
    /**
     * return an object of open documents in the editor.
     * {
     *   '<filepath>': {
     *     filename: str,
     *     unsaved: boolean,
     *     active: boolean,
     *     session: obj (defined by Ace)
     *   },
     *   ...
     * }
     */
    getOpenDocs: function() {
      return openDocs;
    },
    /**
     * The following methods get/set editor settings. The editor settings object
     * is in the following format, with defaults indicated:
     * {
     *   showInvisibles: true,
     *   useSoftTabs: true,
     *   fontSize: 12,
     *   tabSize: 4,
     *   showIndentGuides: true
     * }
     */
    getSettings: function() {
      return editorSettings;
    },
    setSettings: function(settings) {
      editorSettings = settings;
      applySettings();
    },
    /**
     * @ngdoc
     * @name oide.EditorService#openDocument
     * @methodOf oide.EditorService
     *
     * @description
     * Method to open a document in the editor.
     * @example
     * EditorService.openDocument('/path/to/file');
     * @param {str} [filepath] If called with a filepath, that document will be opened or switched to,
     * otherwise a new document will be created and switched to.
     * @returns {str} returns filepath of opened document, or return undefined if opening fails.
     */
    openDocument: function(filepath) {
      if (typeof filepath === 'undefined') {
        // Create an untitled document, and a new editSession to associate it with.
        createUntitledDocument();
      } else {
        if (filepath in openDocs) {
          // Switch to open document
          switchSession(filepath);
        } else {
          // Load document from filesystem
          $log.debug('Load '+filepath+' from filesystem.');
          $http
            .get('/filebrowser/localfiles'+filepath)
            .success(function (data, status, headers, config) {
              var mode = AceModeService.getModeForPath(filepath);
              createNewSession(filepath,data.content,mode.mode);
              switchSession(filepath);
            });
        }
      }
    },
    /**
     * @ngdoc
     * @name oide.EditorService#closeDocument
     * @methodOf oide.EditorService
     *
     * @description
     * Method to close an open document in the editor.
     * @example
     * EditorService.closeDocument('/path/to/file');
     * @param {str} filepath Closes the open document identified by filepath.
     * @returns {str} returns filepath of closed document, or return undefined in case of failure.
     */
    closeDocument: function(filepath) {
      if (filepath in openDocs) {
        delete openDocs[filepath];

        if (Object.keys(openDocs).length !== 0) {
          switchSession(Object.keys(openDocs)[0]);
        }
      }
    },
    /**
     * @ngdoc
     * @name oide.EditorService#saveDocument
     * @methodOf oide.EditorService
     *
     * @description
     * Method to save an open document in the editor.
     * @example
     * EditorService.saveDocument('/path/to/file');
     * @param {str} filepath Saves the open document identified by filepath to the filesystem.
     * @returns {str} returns filepath of saved document, or return undefined in case of failure.
     */
    saveDocument: function(filepath) {
      var content = openDocs[filepath].session.getValue();
      $http
        .get(
          '/filebrowser/a/fileutil',
          {
            params: {
              operation: 'CHECK_EXISTS',
              filepath: filepath
            }
          }
        )
        .success(function (data, status, headers, config) {
          if (data.result) {
            $http({
              url: '/filebrowser/localfiles'+filepath,
              method: 'PUT',
              params: {
                _xsrf: getCookie('_xsrf')
              },
              data: {'content': content}
            })
            .success(function (data,status, headers, config) {
              $log.debug('Saved file: ', filepath);
              openDocs[filepath].unsaved = false;
            });
          } else {
            $http({
              url: '/filebrowser/localfiles'+filepath,
              method: 'POST',
              params: {
                _xsrf: getCookie('_xsrf')
              }
            })
            .success(function (data,status, headers, config) {
              $http({
                url: '/filebrowser/localfiles'+filepath,
                method: 'PUT',
                params: {
                  _xsrf: getCookie('_xsrf')
                },
                data: {'content': content}
              })
              .success(function (data,status, headers, config) {
                $log.debug('Saved file: ', filepath);
                openDocs[filepath].unsaved = false;
              });
            });
          }
        });
    },
    fileRenamed: function(oldpath,newpath) {
      if (oldpath in openDocs) {
        openDocs[newpath] = {
          filepath: newpath,
          filename: getFilenameFromPath(newpath),
          unsaved: openDocs[oldpath].unsaved,
          active: openDocs[oldpath].active,
          session: openDocs[oldpath].session
        };
        var mode = AceModeService.getModeForPath(newpath);
        openDocs[newpath].session.setMode(mode.mode);
        delete openDocs[oldpath];
      }
    },
    fileDeleted: function(filepath) {
      if (filepath in openDocs) {
        openDocs[filepath].unsaved = true;
      }
    },
    applyEditorSettings: function () {
      applySettings();
    },
    openSearchBox: function () {
      editor.execCommand("replace");
    },
    undoChanges: function (filepath) {
      if (filepath in openDocs) {
        var um = openDocs[filepath].session.getUndoManager();
        um.undo();
        openDocs[filepath].session.setUndoManager(um);
      }
    },
    redoChanges: function (filepath) {
      if (filepath in openDocs) {
        var um = openDocs[filepath].session.getUndoManager();
        um.redo();
        openDocs[filepath].session.setUndoManager(um);
      }
    },
    copySelection: function () {
      clipboard = editor.getCopyText();
    },
    cutSelection: function () {
      clipboard = editor.getCopyText();
      editor.insert('');
    },
    pasteClipboard: function () {
      editor.insert(clipboard);
    },
    commentSelection: function () {
      editor.toggleCommentLines();
    }
  };
}]);
