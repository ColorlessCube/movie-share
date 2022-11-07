import {Carousel, Image} from 'antd'
import React, {useEffect} from 'react'
import {useStore} from "../store";


function Recent() {
    const {recentStore} = useStore()


    useEffect(() => {
        recentStore.getRecentMedia({
            offset: 0,
            limit: 10,
            type: 'movie'
        })
    }, [recentStore])

    return (
        <div className='carousel'>
            <Carousel autoplay>
                {recentStore.recentMedias.map(item => {
                    return (
                        <Image
                            src={item.thumb}
                            alt={item.title}
                            width='400px'
                        />
                    )
                })}
            </Carousel>
        </div>
    )
}

export default Recent;