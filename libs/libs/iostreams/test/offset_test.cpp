// (C) Copyright Jonathan Turkanis 2004
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt.)

// See http://www.boost.org/libs/iostreams for documentation.

// Todo: add tests for direct devices.

#include <algorithm>  // equal.
#include <cctype>
#include <iterator>   // back_inserter.
#include <vector>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/device/file.hpp>
#include <boost/iostreams/device/null.hpp>
#include <boost/iostreams/filtering_stream.hpp>
#include <boost/iostreams/offset.hpp>
#include <boost/range/iterator_range.hpp>
#include <boost/test/test_tools.hpp>
#include <boost/test/unit_test.hpp>
#include "detail/constants.hpp"
#include "detail/filters.hpp"
#include "detail/sequence.hpp"
#include "detail/temp_file.hpp"
#include "detail/verification.hpp"

using namespace std;
using namespace boost;
using namespace boost::iostreams;
using namespace boost::iostreams::test;
using boost::unit_test::test_suite;   

const char pad_char = '\n';
const small_padding = 50;
const large_padding = default_device_buffer_size + 50;

void write_padding(std::ofstream& out, int len)
{
    for (int z = 0; z < len; ++z)
        out.put(pad_char);
}

struct offset_test_file : public temp_file {
    offset_test_file(int padding)
        {
            BOOST_IOS::openmode mode = 
                BOOST_IOS::out | BOOST_IOS::binary;
            ::std::ofstream f(name().c_str(), mode);
            write_padding(f, padding);
            const char* buf = narrow_data();
            for (int z = 0; z < data_reps; ++z)
                f.write(buf, data_length());
            write_padding(f, padding);
        }
};

struct offset_test_sequence : public std::vector<char> {
    offset_test_sequence(int padding)
        {
            for (int z = 0; z < padding; ++z)
                push_back(pad_char);
            const char* buf = narrow_data();
            for (int z = 0; z < data_reps; ++z)
                insert(end(), buf, buf + data_length());
            for (int z = 0; z < padding; ++z)
                push_back(pad_char);
        }
};

struct offset_uppercase_file : public temp_file {
    offset_uppercase_file(int padding)
        {
            BOOST_IOS::openmode mode = 
                BOOST_IOS::out | BOOST_IOS::binary;
            ::std::ofstream f(name().c_str(), mode);
            write_padding(f, padding);
            const char* buf = narrow_data();
            for (int z = 0; z < data_reps; ++z)
                for (int w = 0; w < data_length(); ++w)
                    f.put((char) std::toupper(buf[w]));
            write_padding(f, padding);
        }
};

struct offset_lowercase_file : public temp_file {
    offset_lowercase_file(int padding)
        {
            BOOST_IOS::openmode mode = 
                BOOST_IOS::out | BOOST_IOS::binary;
            ::std::ofstream f(name().c_str(), mode);
            write_padding(f, padding);
            const char* buf = narrow_data();
            for (int z = 0; z < data_reps; ++z)
                for (int w = 0; w < data_length(); ++w)
                    f.put((char) std::tolower(buf[w]));
            write_padding(f, padding);
        }
};

// Can't have an offset view of a non-seekble output filter.
struct tolower_seekable_filter : public seekable_filter {
    typedef char char_type;
    struct category 
        : output_seekable,
          filter_tag
        { };
    template<typename Sink>
    bool put(Sink& s, char c)
    { return boost::iostreams::put(s, (char) std::tolower(c)); }

    template<typename Sink>
    stream_offset seek(Sink& s, stream_offset off, BOOST_IOS::seekdir way)
    { return boost::iostreams::seek(s, off, way); }
};

void read_device()
{
    {
        offset_test_file   src1(small_padding);
        test_file          src2;
        stream_offset      off = small_padding,
                           len = data_reps * data_length();
        filtering_istream  first(offset(file_source(src1.name(), in_mode), off, len));
        ifstream           second(src2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed reading from offset_view<Device> with small padding"
        );
    }

    {
        offset_test_file   src1(large_padding);
        test_file          src2;
        stream_offset      off = large_padding,
                           len = data_reps * data_length();
        filtering_istream  first(offset(file_source(src1.name(), in_mode), off, len));
        ifstream           second(src2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed reading from offset_view<Device> with large padding"
        );
    }
}

void read_direct_device()
{
    
    test_sequence<char>   first;
    offset_test_sequence  src(small_padding);
    array_source          array_src(&src[0], &src[0] + src.size());
    stream_offset         off = small_padding,
                          len = data_reps * data_length();
    filtering_istream     second(offset(array_src, off, len));
    BOOST_CHECK_MESSAGE(
        compare_container_and_stream(first, second),
        "failed reading from offset_view<DirectDevice>"
    );
}

void read_filter()
{
    {
        offset_test_file   src1(small_padding);
        uppercase_file     src2;
        stream_offset      off = small_padding,
                           len = data_reps * data_length();
        filtering_istream  first;
        first.push(offset(toupper_filter(), off, len));
        first.push(file_source(src1.name(), in_mode));
        ifstream           second(src2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed reading from an offset_view<Filter> with small padding"
        );
    }

    {
        offset_test_file   src1(large_padding);
        uppercase_file     src2;
        stream_offset      off = large_padding,
                           len = data_reps * data_length();
        filtering_istream  first;
        first.push(offset(toupper_filter(), off, len));
        first.push(file_source(src1.name(), in_mode));
        ifstream           second(src2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed reading from offset_view<Filter> with large padding"
        );
    }
}

void write_device() 
{
    {
        offset_uppercase_file  dest1(small_padding);
        offset_test_file       dest2(small_padding);
        stream_offset          off = small_padding,
                               len = data_reps * data_length();
        filtering_ostream      out(offset(file(dest1.name(), BOOST_IOS::binary), off, len));
        write_data_in_chunks(out);
        out.reset();
        ifstream               first(dest1.name().c_str(), in_mode);
        ifstream               second(dest2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed writing to an offset_view<Device> with small padding"
        );
    }

    {
        offset_uppercase_file  dest1(large_padding);
        offset_test_file       dest2(large_padding);
        stream_offset          off = large_padding,
                               len = data_reps * data_length();
        filtering_ostream      out(offset(file(dest1.name(), BOOST_IOS::binary), off, len));
        write_data_in_chunks(out);
        out.reset();
        ifstream               first(dest1.name().c_str(), in_mode);
        ifstream               second(dest2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed writing to offset_view<Device> with large padding"
        );
    }
}

void write_direct_device() 
{
    vector<char>          dest1(data_reps * data_length() + 2 * small_padding, '\n');
    offset_test_sequence  dest2(small_padding);
    stream_offset         off = small_padding,
                          len = data_reps * data_length();
    array_sink            array(&dest1[0], &dest1[0] + dest1.size());
    filtering_ostream     out(offset(array, off, len));
    write_data_in_chunks(out);
    out.reset();
    BOOST_CHECK_MESSAGE(
        std::equal(dest1.begin(), dest1.end(), dest2.begin()),
        "failed writing to offset_view<DirectDevice>"
    );
}

void write_filter() 
{
    {
        offset_test_file       dest1(small_padding);
        offset_lowercase_file  dest2(small_padding);
        stream_offset          off = small_padding,
                               len = data_reps * data_length();
        filtering_ostream      out;
        out.push(offset(tolower_seekable_filter(), off, len));
        out.push(file(dest1.name(), BOOST_IOS::binary));
        write_data_in_chunks(out);
        out.reset();
        ifstream               first(dest1.name().c_str(), in_mode);
        ifstream               second(dest2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed writing to offset_view<Filter> with small padding"
        );
    }

    {
        offset_test_file       dest1(large_padding);
        offset_lowercase_file  dest2(large_padding);
        stream_offset          off = large_padding,
                               len = data_reps * data_length();
        filtering_ostream      out;
        out.push(offset(tolower_seekable_filter(), off, len));
        out.push(file(dest1.name(), BOOST_IOS::binary));
        write_data_in_chunks(out);
        out.reset();
        ifstream               first(dest1.name().c_str(), in_mode);
        ifstream               second(dest2.name().c_str(), in_mode);
        BOOST_CHECK_MESSAGE(
            compare_streams_in_chunks(first, second),
            "failed writing to offset_view<Filter> with large padding"
        );
    }
}

void seek_device()
{
    offset_test_file           src(small_padding);
    stream_offset              off = large_padding,
                               len = data_reps * data_length();
    filtering_stream<seekable> io(offset(file(src.name(), BOOST_IOS::binary), off, len));
    BOOST_CHECK_MESSAGE(
        test_seekable_in_chars(io),
        "failed seeking within offset_view<Device>"
    );
}

void seek_direct_device()
{
    vector<char>               src(data_reps * data_length() + 2 * small_padding, '\n');
    stream_offset              off = small_padding,
                               len = data_reps * data_length();
    array                      ar(&src[0], &src[0] + src.size());
    filtering_stream<seekable> io(offset(ar, off, len));
    BOOST_CHECK_MESSAGE(
        test_seekable_in_chars(io),
        "failed seeking within offset_view<DirectDevice> with small padding"
    );
}

void seek_filter()
{
    offset_test_file           src(small_padding);
    stream_offset              off = large_padding,
                               len = data_reps * data_length();
    filtering_stream<seekable> io;
    io.push(offset(identity_seekable_filter(), off, len));
    io.push(file(src.name(), BOOST_IOS::binary));
    BOOST_CHECK_MESSAGE(
        test_seekable_in_chars(io),
        "failed seeking within offset_view<Device>"
    );
}

test_suite* init_unit_test_suite(int, char* []) 
{
    test_suite* test = BOOST_TEST_SUITE("offset test");
    test->add(BOOST_TEST_CASE(&read_device));
    test->add(BOOST_TEST_CASE(&read_direct_device));
    test->add(BOOST_TEST_CASE(&read_filter));
    test->add(BOOST_TEST_CASE(&write_device));
    test->add(BOOST_TEST_CASE(&write_direct_device));
    test->add(BOOST_TEST_CASE(&write_filter));
    test->add(BOOST_TEST_CASE(&seek_device));
    test->add(BOOST_TEST_CASE(&seek_direct_device));
    return test;
}
