(function () {

    console.log("LinkedIn Helper Loaded");

    const ID_ICON = "abhijit-linkedin-helper-icon";
    const ID_MENU = "abhijit-linkedin-helper-menu";

    function getProfileData() {

        const text = document.body.innerText;

        const lines = text
            .split("\n")
            .map(x => x.trim())
            .filter(Boolean);

        let fullName = "";
        let company = "";

        for (let i = 0; i < lines.length; i++) {

            if (
                lines[i] === "Message" &&
                lines[i + 1]
            ) {
                fullName = lines[i + 1];
                break;
            }
        }

        for (let i = 0; i < lines.length; i++) {

            if (
                lines[i] === "Contact info" &&
                lines[i + 1]
            ) {
                company = lines[i + 1];
                break;
            }
        }

        if (!fullName) {
            fullName = "Friend";
        }

        if (!company) {
            company = "your company";
        }

        return {
            fullName,
            firstName: fullName.split(" ")[0],
            company
        };
    }

    const templates = {

        referral: (data) => `Hi ${data.firstName}, hope you're doing well!

I'm Abhijit, a Software Engineer with 2 years of experience building scalable backend systems. At Finzly, I've worked on payment rails (Fedwire, RTP, FedNow), ISO 20022 integrations, and recently built an AI-driven regression testing platform using Agentic AI, MCP, and Amazon Bedrock — cutting manual QA effort by 60%.

My core stack is Java, Spring Boot, Microservices, and AWS, with a growing focus on AI-powered backend systems.

I came across the Software Engineer I opening at ${data.company} and it looks like a great fit. Can you please refer me ? I've attached my resume for your reference, and I'd be happy to share anything else you might need.

JD -

Thanks so much for your time — really appreciate it`,

        inquiry: (data) => `Hi ${data.firstName}, hope you're doing well!

I'm Abhijit, a backend Software Engineer with 2 years of experience in Java, Spring Boot, Microservices, and AWS. At my current role, I've built payment processing systems (Fedwire, RTP, FedNow) and an AI-driven testing platform using Agentic AI and Amazon Bedrock — reducing QA cycles by 40%.

I've been genuinely impressed by ${data.company} work and would be grateful if you could let me know of any backend engineering opportunities that may be a good fit for my background.

If there are no suitable openings at present, I completely understand. I would greatly appreciate it if you could keep my resume on file and consider me for future opportunities where my experience may be relevant. Thank you for your time and consideration.

Thanks so much for your time — really appreciate it!

Abhijit Mali
+91 9665754641`
    };

    async function copyTemplate(type) {

        const data = getProfileData();

        const msg = templates[type](data);

        try {

            await navigator.clipboard.writeText(msg);

            console.log(msg);

            autoFillMessageBox(msg);

         

        } catch (e) {

            console.error(e);

            alert("Failed to copy template.");
        }
    }

    function autoFillMessageBox(message) {

        try {

            const editors = document.querySelectorAll(
                '[contenteditable="true"]'
            );

            let editor = null;

            editors.forEach(el => {

                const aria =
                    (el.getAttribute("aria-label") || "")
                        .toLowerCase();

                if (
                    aria.includes("write") ||
                    aria.includes("message") ||
                    aria.includes("compose")
                ) {
                    editor = el;
                }
            });

            if (!editor && editors.length > 0) {
                editor = editors[editors.length - 1];
            }

            if (!editor) {
                return;
            }

            editor.focus();

            editor.textContent = message;

            editor.dispatchEvent(
                new InputEvent(
                    "input",
                    {
                        bubbles: true,
                        cancelable: true
                    }
                )
            );

        } catch (err) {

            console.log(
                "Auto-fill skipped:",
                err
            );
        }
    }

    function toggleMenu() {

        const menu =
            document.getElementById(ID_MENU);

        if (!menu) {
            return;
        }

        menu.style.display =
            menu.style.display === "none"
                ? "block"
                : "none";
    }

    function createMenu() {

        const menu =
            document.createElement("div");

        menu.id = ID_MENU;

        menu.style.position = "fixed";
        menu.style.right = "20px";
        menu.style.bottom = "200px";
        menu.style.width = "220px";
        menu.style.background = "#fff";
        menu.style.border = "1px solid #ddd";
        menu.style.borderRadius = "12px";
        menu.style.boxShadow =
            "0 4px 16px rgba(0,0,0,.15)";
        menu.style.padding = "10px";
        menu.style.zIndex = "999999";
        menu.style.display = "none";
        menu.style.fontFamily =
            "Arial, sans-serif";

        const title =
            document.createElement("div");

        title.innerText =
            "LinkedIn Helper";

        title.style.fontWeight = "bold";
        title.style.marginBottom = "10px";

        const referralBtn =
            document.createElement("button");

        referralBtn.innerText =
            "📋 Copy Referral";

        referralBtn.style.width = "100%";
        referralBtn.style.marginBottom = "8px";
        referralBtn.style.padding = "10px";
        referralBtn.style.cursor = "pointer";

        referralBtn.onclick =
            () => copyTemplate("referral");

        const inquiryBtn =
            document.createElement("button");

        inquiryBtn.innerText =
            "📋 Copy Inquiry";

        inquiryBtn.style.width = "100%";
        inquiryBtn.style.padding = "10px";
        inquiryBtn.style.cursor = "pointer";

        inquiryBtn.onclick =
            () => copyTemplate("inquiry");

        menu.appendChild(title);
        menu.appendChild(referralBtn);
        menu.appendChild(inquiryBtn);

        document.body.appendChild(menu);
    }

    function createFloatingIcon() {

        if (
            document.getElementById(ID_ICON)
        ) {
            return;
        }

        const btn =
            document.createElement("div");

        btn.id = ID_ICON;

        btn.innerHTML = "🚀";

        btn.style.position = "fixed";
        btn.style.right = "20px";
        btn.style.bottom = "140px";
        btn.style.width = "52px";
        btn.style.height = "52px";
        btn.style.borderRadius = "50%";
        btn.style.background = "#0A66C2";
        btn.style.color = "#fff";
        btn.style.display = "flex";
        btn.style.alignItems = "center";
        btn.style.justifyContent = "center";
        btn.style.fontSize = "24px";
        btn.style.cursor = "pointer";
        btn.style.zIndex = "999999";
        btn.style.boxShadow =
            "0 4px 12px rgba(0,0,0,.25)";

        btn.onclick = toggleMenu;

        document.body.appendChild(btn);

        createMenu();
    }

    setTimeout(
        createFloatingIcon,
        3000
    );

})();