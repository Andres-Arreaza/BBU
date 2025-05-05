// Layout.js
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Doctors } from "./pages/doctors";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import injectContext from "./store/appContext";

import { DoctorProfile } from "./component/doctorProfile";
import { DoctorList } from "./component/doctorList";
import { Schedule } from "./component/schedule";
import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";
import { SingleLogin } from "./pages/Auth/singleLogin";
import SingleSignup from "./pages/Auth/singleSignup";
import StartHome from "./component/StartHome";
import { Home } from "./pages/Home";
import CreateTestimony from "./pages/CreateTestimony";
import Testimonials from "./component/Testimonials";

import MedicalHistory from "./pages/MedicalHistory";
import CreateMedicalHistory from "./pages/CreateMedicalHistory";
import ViewPatients from "./pages/ViewPatients";
import ViewMedicalHistory from "./pages/ViewMedicalHistory";
import PatientMedicalHistory from "./pages/PatientMedicalHistory";
import ViewDoctors from "./pages/ViewDoctors";
import DoctorMedicalHistories from "./pages/DoctorMedicalHistories";

const Layout = () => {
    const basename = process.env.BASENAME || "";

    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === "") return <BackendURL />;

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
                    <Routes>
                        <Route element={<Doctors />} path="/doctors" />
                        <Route element={<DoctorProfile />} path="/doctors/:id" />
                        <Route element={<DoctorList />} path="/doctors" />
                        <Route element={<Schedule />} path="/appointment" />
                        <Route element={<Demo />} path="/demo" />
                        <Route element={<Single />} path="/single/:theid" />
                        <Route element={<h1>Not found!</h1>} path="*" />
                        <Route element={<SingleLogin />} path="/login" />
                        <Route element={<SingleSignup />} path="/signup" />
                        <Route element={<CreateTestimony />} path="/testimonials" />
                        <Route path="/create-medical-history" element={<CreateMedicalHistory />} />
                        <Route path="/view-patients" element={<ViewPatients />} />
                        <Route path="/patient-history/:id" element={<PatientMedicalHistory />} />
                        <Route path="/view-medical-history" element={<ViewMedicalHistory />} />
                        <Route path="/medical-history" element={<MedicalHistory />} />
                        <Route path="/view-doctors" element={<ViewDoctors />} />
                        <Route path="/doctor-medical-histories/:doctorId" element={<DoctorMedicalHistories />} />
                        <Route element={<Home />} path="/" />
                    </Routes>
                    {/* <Footer /> */}
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);
