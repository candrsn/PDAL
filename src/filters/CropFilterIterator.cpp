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

#include <libpc/filters/CropFilterIterator.hpp>
#include <libpc/filters/CropFilter.hpp>
#include <libpc/exceptions.hpp>

namespace libpc { namespace filters {


CropFilterIterator::CropFilterIterator(const CropFilter& filter)
    : libpc::FilterIterator(filter)
    , m_stageAsDerived(filter)
{
    return;
}


void CropFilterIterator::seekToPoint(boost::uint64_t pointNum)
{
    // getPrevIterator().seekToPoint(pointNum);
}


boost::uint32_t CropFilterIterator::readBuffer(PointBuffer& data)
{
    CropFilter& filter = const_cast<CropFilter&>(m_stageAsDerived);       // BUG BUG BUG

    PointBuffer srcData(data.getSchemaLayout(), data.getCapacity());

    boost::uint32_t numSrcPointsRead = getPrevIterator().read(srcData);
    if (numSrcPointsRead == 0) return 0;

    const SchemaLayout& schemaLayout = data.getSchemaLayout();
    const Schema& schema = schemaLayout.getSchema();

    int fieldX = schema.getDimensionIndex(Dimension::Field_X);
    int fieldY = schema.getDimensionIndex(Dimension::Field_Y);
    int fieldZ = schema.getDimensionIndex(Dimension::Field_Z);

    boost::uint32_t numPoints = data.getCapacity();
    
    const Bounds<double>& bounds = filter.getBounds();

    boost::uint32_t srcIndex = 0;
    boost::uint32_t dstIndex = 0;
    for (srcIndex=0; srcIndex<numPoints; srcIndex++)
    {
    
        double x = srcData.getField<double>(srcIndex, fieldX);
        double y = srcData.getField<double>(srcIndex, fieldY);
        double z = srcData.getField<double>(srcIndex, fieldZ);
        Vector<double> point(x,y,z);
        
        if (bounds.contains(point))
        {
            data.copyPointFast(dstIndex, srcIndex, srcData);
            data.setNumPoints(dstIndex+1);
            dstIndex += 1;
            
        }
    }
    
    
    incrementCurrentPointIndex(numPoints);

    return data.getNumPoints();
}


} } // namespaces
