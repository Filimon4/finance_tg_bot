import React from "react"
import styles from './maincontainer.module.scss'

export const MainContainer = ({children}: {children: React.ReactNode}) => {
    return (
        <div className={`w-screen h-screen ${styles.container} px-auto`}>
            <div className="max-w-[500px] w-full h-full m-auto">
                {children}
            </div>
        </div>
    )
}
