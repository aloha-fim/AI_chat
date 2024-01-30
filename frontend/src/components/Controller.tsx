import { useState } from "react";
import Title from "./Title";
import axios from "axios";
import RecordMessage from "./RecordMessage";

function Controller() {
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<any[]>([]);

    function createBlobURL(data: any) {
        const blob = new Blob([data], { type: "audio/mpeg"});
        const url = window.URL.createObjectURL(blob);
        return url;
    };

    const handleStop = async (blobUrl: string) => {
        console.log(blobUrl);
        setIsLoading(true);

        //Append recorded message to messages
        const myMessage = { sender: "me", blobUrl };
        const messagesArr = [...messages, myMessage];

        // convert blob url to blob object
        fetch(blobUrl)
            .then((res) => res.blob())
            .then(async (blob) => {
                // construct audio to send file
                const formData = new FormData();
                formData.append("file", blob, "myFile.wav");

                // send form data to api endpoint
                await axios.post("http://localhost:8000/post-audio", formData, {
                    headers: {
                        "Content-Type": "audio/mpeg",
                    },
                    responseType: "arraybuffer", // set the response type to handle binary data
                })
                .then((res: any) => {
                    const blob = res.data;
                    const audio = new Audio();
                    audio.src = createBlobURL(blob);

                    // append to audio
                    const shaunMessage = { sender: "shaun", blobUrl: audio.src };
                    messagesArr.push(shaunMessage);
                    setMessages(messagesArr);

                    // play audio
                    setIsLoading(fales);
                    audio.play();
                })
                .catch((err: any) => {
                    console.error(err);
                    setIsLoading(false);
                });
            });
    };

    return (
        <div className="h-screen overflow-y-hidden">
            {/* Title */}
            <Title setMessages={setMessages} />

            <div className="flex flex-col justify-between h-full overflow-y-scroll pb96">
                {/* Conversation */}
                <div className="mt-5 px-5">
                    {messages?.map((audio, index) => {
                        return (
                            <div
                                key={index + audio.sender}
                                className={
                                    "flex flex-col " +
                                    (audio.sender == "shaun" && "flex items-end")
                                }
                            >
                                {/* Sender */}
                                <div className="mt-4">
                                    <p
                                        className={
                                            audio.sender == "shaun"
                                                ? "text-right mr-2 italic text-green-500"
                                                : "ml-2 italic text-blue-500"
                                        }
                                    >
                                        {audio.sender}
                                    </p>

                                    {/* Message */}
                                    <audio
                                        src={audio.blobUrl}
                                        className="appearance-none"
                                        controls
                                    />
                                </div>
                            </div>
                        );
                    })}

                    {messages.length == 0 && !isLoading && (
                        <div className="text-center font-light italic mt-10">
                            Send Shaun a message...
                        </div>
                    )}

                    {isLoading && (
                        <div className="text-center font-light italic mt-10 animate-pulse">
                            Processing...
                        </div>
                    )}
                </div>

                {/* Recorder */}
                <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 text-blue-500">
                    <div className="flex justify-center items-center w-full">
                        <div>
                            <RecordMessage handlestop={handleStop} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Controller;