cmake_minimum_required(VERSION 3.6)
project(src)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    char_property.cpp
    char_property.h
    common.h
    connector.cpp
    connector.h
    context_id.cpp
    context_id.h
    darts.h
    dictionary.cpp
    dictionary.h
    dictionary_compiler.cpp
    dictionary_generator.cpp
    dictionary_rewriter.cpp
    dictionary_rewriter.h
    eval.cpp
    feature_index.cpp
    feature_index.h
    freelist.h
    iconv_utils.cpp
    iconv_utils.h
    lbfgs.cpp
    lbfgs.h
    learner.cpp
    learner_node.h
    learner_tagger.cpp
    learner_tagger.h
    libmecab.cpp
    mecab-cost-train.cpp
    mecab-dict-gen.cpp
    mecab-dict-index.cpp
    mecab-system-eval.cpp
    mecab-test-gen.cpp
    mecab.cpp
    mecab.h
    mmap.h
    nbest_generator.cpp
    nbest_generator.h
    param.cpp
    param.h
    scoped_ptr.h
    stream_wrapper.h
    string_buffer.cpp
    string_buffer.h
    tagger.cpp
    thread.h
    tokenizer.cpp
    tokenizer.h
    ucs.h
    ucstable.h
    utils.cpp
    utils.h
    viterbi.cpp
    viterbi.h
    winmain.h
    writer.cpp
    writer.h)

add_executable(src ${SOURCE_FILES})