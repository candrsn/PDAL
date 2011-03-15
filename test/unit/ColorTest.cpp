/******************************************************************************
* Copyright (c) 2011, Michael P. Gerlek (mpg@flaxen.com)
*
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following
* conditions are met:
*
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in
*       the documentation and/or other materials provided
*       with the distribution.
*     * Neither the name of Hobu, Inc. or Flaxen Geo Consulting nor the
*       names of its contributors may be used to endorse or promote
*       products derived from this software without specific prior
*       written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
* FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
* COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
* BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
* OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
* AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
* OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
* OF SUCH DAMAGE.
****************************************************************************/

#include <boost/test/unit_test.hpp>
#include <boost/cstdint.hpp>

#include <libpc/Color.hpp>

using namespace libpc;

BOOST_AUTO_TEST_SUITE(ColorTest)

BOOST_AUTO_TEST_CASE(test_ctor)
{
    Color c0;
    Color c1(1,2,3);
    boost::array<boost::uint16_t,3> a = {{1,2,3}};
    Color c2(a);
    Color c3(c2);
    Color c4 = c3;

    BOOST_CHECK(c2!=c0);
    BOOST_CHECK(c2==c1);
    BOOST_CHECK(c2==c2);
    BOOST_CHECK(c3==c2);
    BOOST_CHECK(c4==c2);
}

BOOST_AUTO_TEST_CASE(test_accessors)
{
  Color c0;
  BOOST_CHECK(c0[0]==0);
  BOOST_CHECK(c0[1]==0);
  BOOST_CHECK(c0[2]==0);

  Color c1(1,2,3);
  BOOST_CHECK(c1[0]==1);
  BOOST_CHECK(c1[1]==2);
  BOOST_CHECK(c1[2]==3);
  
  BOOST_CHECK(c1.getRed()==1);
  BOOST_CHECK(c1.getGreen()==2);
  BOOST_CHECK(c1.getBlue()==3);

  c0.setRed(1);
  c0.setGreen(2);
  c0.setBlue(3);

  BOOST_CHECK(c0 == c1);
}


// BUG: interpolate function not tested

BOOST_AUTO_TEST_SUITE_END()
