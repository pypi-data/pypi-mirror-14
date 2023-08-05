/*
Copyright 2015 Google Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef JSONNET_STRING_H
#define JSONNET_STRING_H

#include "lexer.h"

/** Unparse the string. */
String jsonnet_string_unparse(const String &str, bool single);

/** Escape special characters. */
String jsonnet_string_escape(const String &str, bool single);

/** Resolve escape chracters in the string. */
String jsonnet_string_unescape(const LocationRange &loc, const String &s);

#endif
